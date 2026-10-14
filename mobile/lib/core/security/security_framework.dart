import 'package:dio/dio.dart';
import '../config/security_config.dart';
import '../constants/api_constants.dart';
import '../network/api_client.dart';
import '../storage/token_manager.dart';
import '../utils/device_fingerprint.dart';
import '../utils/security_logger.dart';
import 'models/pinning_config.dart';
import 'models/security_event.dart';
import 'models/security_status.dart';
import 'providers/flutter_secure_storage_provider.dart';
import 'providers/method_channel_runtime_security_provider.dart';
import 'providers/offline_security_event_queue.dart';
import 'providers/risk_evaluation_provider.dart';
import 'providers/runtime_security_provider.dart';
import 'providers/secure_storage_provider.dart';
import 'providers/security_event_reporter.dart';
import 'providers/security_event_reporter_impl.dart';

/// Master orchestrator for the Reusable Mobile Security Framework.
///
/// Any client application can initialize and interact with the framework through this unified API.
class SecurityFramework {
  final SecurityConfig config;
  final SecureStorageProvider secureStorage;
  final RuntimeSecurityProvider runtimeSecurity;
  final SecurityEventReporter eventReporter;
  final TokenManager tokenManager;
  final String deviceId;
  final SecurityLogger _logger;

  SecurityStatus? _lastKnownStatus;

  SecurityFramework._({
    required this.config,
    required this.secureStorage,
    required this.runtimeSecurity,
    required this.eventReporter,
    required this.tokenManager,
    required this.deviceId,
    SecurityLogger? logger,
  }) : _logger = logger ?? const SecurityLogger();

  /// Initializes the complete security framework, setting up Keystore/Keychain, RASP probes, and event queues.
  static Future<SecurityFramework> initialize({
    SecurityConfig? config,
    SecureStorageProvider? storage,
    RuntimeSecurityProvider? runtimeSecurity,
    SecurityEventReporter? eventReporter,
    String? customDeviceId,
    String? apiBaseUrl,
  }) async {
    final effectiveConfig = config ?? const SecurityConfig();
    final effectiveStorage = storage ?? FlutterSecureStorageProvider();
    final effectiveTokenManager = TokenManager(effectiveStorage);

    // Resolve or generate deterministic device identifier
    final deviceFingerprint = DeviceFingerprint(effectiveStorage);
    final resolvedDeviceId = customDeviceId ?? await deviceFingerprint.getDeviceId();

    final effectiveRuntime = runtimeSecurity ??
        MethodChannelRuntimeSecurityProvider(
          deviceId: resolvedDeviceId,
          riskEvaluator: const RiskEvaluationProvider(),
        );

    final effectiveReporter = eventReporter ??
        SecurityEventReporterImpl(
          dio: Dio(
            BaseOptions(
              baseUrl: apiBaseUrl ?? ApiConstants.defaultBaseUrl,
              connectTimeout: ApiConstants.connectTimeout,
              receiveTimeout: ApiConstants.receiveTimeout,
            ),
          ),
          queue: OfflineSecurityEventQueue(),
        );

    final framework = SecurityFramework._(
      config: effectiveConfig,
      secureStorage: effectiveStorage,
      runtimeSecurity: effectiveRuntime,
      eventReporter: effectiveReporter,
      tokenManager: effectiveTokenManager,
      deviceId: resolvedDeviceId,
    );

    framework._logger.info(
      'SecurityFramework initialized successfully for device: $resolvedDeviceId',
    );

    return framework;
  }

  /// Performs a live RASP diagnostic check across all configured probes.
  Future<SecurityStatus> checkRuntimeSecurity() async {
    _logger.info('Executing live RASP diagnostic checks...');
    final status = await runtimeSecurity.getSecurityStatus();
    _lastKnownStatus = status;

    // Automated telemetry dispatch if threats are discovered
    if (status.detectedThreats.isNotEmpty &&
        config.securityEventReportingEnabled) {
      for (final threat in status.detectedThreats) {
        await reportThreatDetected(
          eventType: threat,
          severity: status.riskLevel.toProtocolString(),
          description: 'Runtime probe triggered on ${status.platform}: $threat',
          metadata: {
            'riskScore': status.riskLevel.numericalScore,
            'rootDetected': status.rootDetected,
            'jailbreakDetected': status.jailbreakDetected,
            'emulatorDetected': status.emulatorDetected,
            'debuggerDetected': status.debuggerDetected,
            'fridaDetected': status.fridaDetected,
          },
        );
      }
    }

    return status;
  }

  /// Returns cached or fresh security status.
  Future<SecurityStatus> getSecurityStatus() async {
    if (_lastKnownStatus != null) {
      return _lastKnownStatus!;
    }
    return await checkRuntimeSecurity();
  }

  /// Reports a custom security event into the threat pipeline.
  Future<void> reportSecurityEvent(SecurityEvent event) async {
    await eventReporter.reportEvent(event);
  }

  /// Helper reporting a detected threat by event type.
  Future<void> reportThreatDetected({
    required String eventType,
    required String severity,
    required String description,
    Map<String, dynamic>? metadata,
  }) async {
    final currentUserId = await tokenManager.getUserId();
    final event = SecurityEvent(
      userId: currentUserId,
      deviceId: deviceId,
      eventType: eventType,
      severity: severity,
      source: 'MOBILE_RASP',
      description: description,
      metadata: metadata ?? {},
    );

    await reportSecurityEvent(event);
  }

  /// Factory creating an authenticated, pinned [ApiClient] tied to this framework instance.
  ApiClient createSecureApiClient({
    required String baseUrl,
    PinningConfig? pinningConfig,
  }) {
    return ApiClient(
      baseUrl: baseUrl,
      tokenManager: tokenManager,
      deviceId: deviceId,
      securityConfig: config,
      pinningConfig: pinningConfig,
    );
  }

  /// Clears in-memory and keystore session state (e.g., on logout or CRITICAL threat).
  Future<void> wipeSession() async {
    _logger.warn('Wiping active session credentials from device keystore...');
    await tokenManager.clearSession();
  }
}
