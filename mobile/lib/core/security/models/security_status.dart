import 'dart:convert';
import 'risk_level.dart';

/// Comprehensive snapshot of device runtime security state.
class SecurityStatus {
  final bool rootDetected;
  final bool jailbreakDetected;
  final bool emulatorDetected;
  final bool simulatorDetected;
  final bool debuggerDetected;
  final bool fridaDetected;
  final bool integrityValid;
  final bool sslPinningEnabled;
  final bool secureStorageAvailable;
  final RiskLevel riskLevel;
  final List<String> detectedThreats;
  final DateTime timestamp;
  final String deviceId;
  final String platform;

  const SecurityStatus({
    required this.rootDetected,
    required this.jailbreakDetected,
    required this.emulatorDetected,
    required this.simulatorDetected,
    required this.debuggerDetected,
    required this.fridaDetected,
    required this.integrityValid,
    required this.sslPinningEnabled,
    required this.secureStorageAvailable,
    required this.riskLevel,
    required this.detectedThreats,
    required this.timestamp,
    required this.deviceId,
    required this.platform,
  });

  /// Factory producing a clean initial baseline status.
  factory SecurityStatus.clean({
    required String deviceId,
    required String platform,
  }) {
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
      deviceId: deviceId,
      platform: platform,
    );
  }

  /// Whether any active threat was detected that compromises the host.
  bool get isCompromised =>
      rootDetected ||
      jailbreakDetected ||
      debuggerDetected ||
      fridaDetected ||
      !integrityValid ||
      riskLevel == RiskLevel.critical;

  int get threatCount => detectedThreats.length;

  Map<String, dynamic> toMap() {
    return {
      'rootDetected': rootDetected,
      'jailbreakDetected': jailbreakDetected,
      'emulatorDetected': emulatorDetected,
      'simulatorDetected': simulatorDetected,
      'debuggerDetected': debuggerDetected,
      'fridaDetected': fridaDetected,
      'integrityValid': integrityValid,
      'sslPinningEnabled': sslPinningEnabled,
      'secureStorageAvailable': secureStorageAvailable,
      'riskLevel': riskLevel.toProtocolString(),
      'detectedThreats': detectedThreats,
      'timestamp': timestamp.toIso8601String(),
      'deviceId': deviceId,
      'platform': platform,
    };
  }

  factory SecurityStatus.fromMap(Map<String, dynamic> map) {
    return SecurityStatus(
      rootDetected: map['rootDetected'] as bool? ?? false,
      jailbreakDetected: map['jailbreakDetected'] as bool? ?? false,
      emulatorDetected: map['emulatorDetected'] as bool? ?? false,
      simulatorDetected: map['simulatorDetected'] as bool? ?? false,
      debuggerDetected: map['debuggerDetected'] as bool? ?? false,
      fridaDetected: map['fridaDetected'] as bool? ?? false,
      integrityValid: map['integrityValid'] as bool? ?? true,
      sslPinningEnabled: map['sslPinningEnabled'] as bool? ?? true,
      secureStorageAvailable: map['secureStorageAvailable'] as bool? ?? true,
      riskLevel: RiskLevel.fromString(map['riskLevel'] as String?),
      detectedThreats: List<String>.from(map['detectedThreats'] as List? ?? []),
      timestamp: map['timestamp'] != null
          ? DateTime.parse(map['timestamp'] as String)
          : DateTime.now().toUtc(),
      deviceId: map['deviceId'] as String? ?? 'unknown-device',
      platform: map['platform'] as String? ?? 'generic',
    );
  }

  String toJson() => jsonEncode(toMap());

  factory SecurityStatus.fromJson(String source) =>
      SecurityStatus.fromMap(jsonDecode(source) as Map<String, dynamic>);

  SecurityStatus copyWith({
    bool? rootDetected,
    bool? jailbreakDetected,
    bool? emulatorDetected,
    bool? simulatorDetected,
    bool? debuggerDetected,
    bool? fridaDetected,
    bool? integrityValid,
    bool? sslPinningEnabled,
    bool? secureStorageAvailable,
    RiskLevel? riskLevel,
    List<String>? detectedThreats,
    DateTime? timestamp,
    String? deviceId,
    String? platform,
  }) {
    return SecurityStatus(
      rootDetected: rootDetected ?? this.rootDetected,
      jailbreakDetected: jailbreakDetected ?? this.jailbreakDetected,
      emulatorDetected: emulatorDetected ?? this.emulatorDetected,
      simulatorDetected: simulatorDetected ?? this.simulatorDetected,
      debuggerDetected: debuggerDetected ?? this.debuggerDetected,
      fridaDetected: fridaDetected ?? this.fridaDetected,
      integrityValid: integrityValid ?? this.integrityValid,
      sslPinningEnabled: sslPinningEnabled ?? this.sslPinningEnabled,
      secureStorageAvailable:
          secureStorageAvailable ?? this.secureStorageAvailable,
      riskLevel: riskLevel ?? this.riskLevel,
      detectedThreats: detectedThreats ?? this.detectedThreats,
      timestamp: timestamp ?? this.timestamp,
      deviceId: deviceId ?? this.deviceId,
      platform: platform ?? this.platform,
    );
  }
}
