import 'dart:io' show Platform;
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/services.dart';
import '../../constants/security_constants.dart';
import '../models/risk_level.dart';
import '../models/security_status.dart';
import 'risk_evaluation_provider.dart';
import 'runtime_security_provider.dart';

/// Implementation of [RuntimeSecurityProvider] delegating to native Kotlin & Swift via MethodChannel.
class MethodChannelRuntimeSecurityProvider implements RuntimeSecurityProvider {
  final MethodChannel _channel;
  final RiskEvaluationProvider _riskEvaluator;
  final String _deviceId;

  MethodChannelRuntimeSecurityProvider({
    MethodChannel? channel,
    RiskEvaluationProvider? riskEvaluator,
    required String deviceId,
  })  : _channel = channel ??
            const MethodChannel(SecurityConstants.runtimeProtectionChannel),
        _riskEvaluator = riskEvaluator ?? const RiskEvaluationProvider(),
        _deviceId = deviceId;

  @override
  Future<bool> checkRootOrJailbreak() async {
    try {
      final bool? result =
          await _channel.invokeMethod<bool>('checkRootOrJailbreak');
      return result ?? false;
    } on PlatformException {
      return false;
    } on MissingPluginException {
      // In testing/desktop environments where native plugin is not registered
      return false;
    }
  }

  @override
  Future<bool> checkEmulatorOrSimulator() async {
    try {
      final bool? result =
          await _channel.invokeMethod<bool>('checkEmulatorOrSimulator');
      return result ?? false;
    } on PlatformException {
      return false;
    } on MissingPluginException {
      return false;
    }
  }

  @override
  Future<bool> checkDebuggerAttached() async {
    try {
      final bool? result =
          await _channel.invokeMethod<bool>('checkDebuggerAttached');
      return result ?? false;
    } on PlatformException {
      return false;
    } on MissingPluginException {
      return false;
    }
  }

  @override
  Future<bool> checkFridaOrInstrumentation() async {
    try {
      final bool? result = await _channel.invokeMethod<bool>('checkFrida');
      return result ?? false;
    } on PlatformException {
      return false;
    } on MissingPluginException {
      return false;
    }
  }

  @override
  Future<bool> verifyAppIntegrity({String? expectedSignature}) async {
    try {
      final bool? result = await _channel.invokeMethod<bool>(
        'verifyIntegrity',
        {'expectedSignature': expectedSignature},
      );
      return result ?? true;
    } on PlatformException {
      return true;
    } on MissingPluginException {
      return true;
    }
  }

  @override
  Future<SecurityStatus> getSecurityStatus() async {
    if (kIsWeb) {
      return SecurityStatus(
        rootDetected: false,
        jailbreakDetected: false,
        emulatorDetected: false,
        simulatorDetected: false,
        debuggerDetected: false,
        fridaDetected: false,
        integrityValid: true,
        sslPinningEnabled: true,
        secureStorageAvailable: true,
        riskLevel: RiskLevel.low,
        detectedThreats: const [],
        timestamp: DateTime.now().toUtc(),
        deviceId: _deviceId,
        platform: 'ios',
      );
    }

    String platformName = 'desktop';
    bool isAndroid = false;
    try {
      isAndroid = Platform.isAndroid;
      platformName = isAndroid ? 'android' : (Platform.isIOS ? 'ios' : 'desktop');
    } catch (_) {
      platformName = 'ios';
    }

    try {
      final dynamic rawMap =
          await _channel.invokeMethod<dynamic>('getComprehensiveStatus');

      if (rawMap is Map) {
        final Map<String, dynamic> map = Map<String, dynamic>.from(rawMap);
        final bool root = map['rootDetected'] as bool? ?? false;
        final bool jailbreak = map['jailbreakDetected'] as bool? ?? false;
        final bool emulator = map['emulatorDetected'] as bool? ?? false;
        final bool simulator = map['simulatorDetected'] as bool? ?? false;
        final bool debugger = map['debuggerDetected'] as bool? ?? false;
        final bool frida = map['fridaDetected'] as bool? ?? false;
        final bool integrity = map['integrityValid'] as bool? ?? true;
        final bool sslPinning = map['sslPinningEnabled'] as bool? ?? true;
        final bool secureStore = map['secureStorageAvailable'] as bool? ?? true;

        final List<String> threats = <String>[];
        if (root) threats.add(SecurityConstants.eventRootDetected);
        if (jailbreak) threats.add(SecurityConstants.eventJailbreakDetected);
        if (emulator) threats.add(SecurityConstants.eventEmulatorDetected);
        if (simulator) threats.add(SecurityConstants.eventSimulatorDetected);
        if (debugger) threats.add(SecurityConstants.eventDebuggerDetected);
        if (frida) threats.add(SecurityConstants.eventFridaDetected);
        if (!integrity) threats.add(SecurityConstants.eventIntegrityFailure);

        final RiskLevel computedRisk = _riskEvaluator.evaluateThreats(threats);

        return SecurityStatus(
          rootDetected: root,
          jailbreakDetected: jailbreak,
          emulatorDetected: emulator,
          simulatorDetected: simulator,
          debuggerDetected: debugger,
          fridaDetected: frida,
          integrityValid: integrity,
          sslPinningEnabled: sslPinning,
          secureStorageAvailable: secureStore,
          riskLevel: computedRisk,
          detectedThreats: threats,
          timestamp: DateTime.now().toUtc(),
          deviceId: _deviceId,
          platform: platformName,
        );
      }
    } catch (_) {
      // Fall through to manual probe aggregation
    }

    // Fallback: Query individual probes concurrently
    final List<bool> results = await Future.wait([
      checkRootOrJailbreak(),
      checkEmulatorOrSimulator(),
      checkDebuggerAttached(),
      checkFridaOrInstrumentation(),
      verifyAppIntegrity(),
    ]);

    final bool rootOrJailbreak = results[0];
    final bool emulatorOrSimulator = results[1];
    final bool debugger = results[2];
    final bool frida = results[3];
    final bool integrity = results[4];

    final bool root = isAndroid && rootOrJailbreak;
    final bool jailbreak = !isAndroid && rootOrJailbreak;
    final bool emulator = isAndroid && emulatorOrSimulator;
    final bool simulator = !isAndroid && emulatorOrSimulator;

    final List<String> threats = <String>[];
    if (root) threats.add(SecurityConstants.eventRootDetected);
    if (jailbreak) threats.add(SecurityConstants.eventJailbreakDetected);
    if (emulator) threats.add(SecurityConstants.eventEmulatorDetected);
    if (simulator) threats.add(SecurityConstants.eventSimulatorDetected);
    if (debugger) threats.add(SecurityConstants.eventDebuggerDetected);
    if (frida) threats.add(SecurityConstants.eventFridaDetected);
    if (!integrity) threats.add(SecurityConstants.eventIntegrityFailure);

    final RiskLevel computedRisk = _riskEvaluator.evaluateThreats(threats);

    return SecurityStatus(
      rootDetected: root,
      jailbreakDetected: jailbreak,
      emulatorDetected: emulator,
      simulatorDetected: simulator,
      debuggerDetected: debugger,
      fridaDetected: frida,
      integrityValid: integrity,
      sslPinningEnabled: true,
      secureStorageAvailable: true,
      riskLevel: computedRisk,
      detectedThreats: threats,
      timestamp: DateTime.now().toUtc(),
      deviceId: _deviceId,
      platform: platformName,
    );
  }
}
