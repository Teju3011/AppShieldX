import 'dart:convert';

/// Configuration model governing client-side runtime protection policies.
class SecurityConfig {
  final bool runtimeProtectionEnabled;
  final bool rootDetectionEnabled;
  final bool jailbreakDetectionEnabled;
  final bool emulatorDetectionEnabled;
  final bool debuggerDetectionEnabled;
  final bool fridaDetectionEnabled;
  final bool integrityCheckEnabled;
  final bool certificatePinningEnabled;
  final bool biometricEnabled;
  final bool securityEventReportingEnabled;
  final String riskThreshold; // "LOW", "MEDIUM", "HIGH", "CRITICAL"
  final int sessionTimeoutSeconds;
  final List<String> pinnedCertificatesSHA256;

  const SecurityConfig({
    this.runtimeProtectionEnabled = true,
    this.rootDetectionEnabled = true,
    this.jailbreakDetectionEnabled = true,
    this.emulatorDetectionEnabled = true,
    this.debuggerDetectionEnabled = true,
    this.fridaDetectionEnabled = true,
    this.integrityCheckEnabled = true,
    this.certificatePinningEnabled = false, // Configurable for dev/prod
    this.biometricEnabled = true,
    this.securityEventReportingEnabled = true,
    this.riskThreshold = 'MEDIUM',
    this.sessionTimeoutSeconds = 900,
    this.pinnedCertificatesSHA256 = const [],
  });

  /// Factory creating strict production-grade security configuration.
  factory SecurityConfig.production({
    required List<String> pinnedCertificatesSHA256,
  }) {
    return SecurityConfig(
      runtimeProtectionEnabled: true,
      rootDetectionEnabled: true,
      jailbreakDetectionEnabled: true,
      emulatorDetectionEnabled: true,
      debuggerDetectionEnabled: true,
      fridaDetectionEnabled: true,
      integrityCheckEnabled: true,
      certificatePinningEnabled: true,
      biometricEnabled: true,
      securityEventReportingEnabled: true,
      riskThreshold: 'HIGH',
      sessionTimeoutSeconds: 600,
      pinnedCertificatesSHA256: pinnedCertificatesSHA256,
    );
  }

  /// Factory creating permissive configuration for development and emulator verification.
  factory SecurityConfig.development({
    String riskThreshold = 'MEDIUM',
    bool emulatorDetectionEnabled = false,
    bool debuggerDetectionEnabled = false,
  }) {
    return SecurityConfig(
      runtimeProtectionEnabled: true,
      rootDetectionEnabled: true,
      jailbreakDetectionEnabled: true,
      emulatorDetectionEnabled: emulatorDetectionEnabled,
      debuggerDetectionEnabled: debuggerDetectionEnabled,
      fridaDetectionEnabled: true,
      integrityCheckEnabled: false,
      certificatePinningEnabled: false,
      biometricEnabled: false,
      securityEventReportingEnabled: true,
      riskThreshold: riskThreshold,
      sessionTimeoutSeconds: 3600,
      pinnedCertificatesSHA256: const [],
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'runtimeProtectionEnabled': runtimeProtectionEnabled,
      'rootDetectionEnabled': rootDetectionEnabled,
      'jailbreakDetectionEnabled': jailbreakDetectionEnabled,
      'emulatorDetectionEnabled': emulatorDetectionEnabled,
      'debuggerDetectionEnabled': debuggerDetectionEnabled,
      'fridaDetectionEnabled': fridaDetectionEnabled,
      'integrityCheckEnabled': integrityCheckEnabled,
      'certificatePinningEnabled': certificatePinningEnabled,
      'biometricEnabled': biometricEnabled,
      'securityEventReportingEnabled': securityEventReportingEnabled,
      'riskThreshold': riskThreshold,
      'sessionTimeoutSeconds': sessionTimeoutSeconds,
      'pinnedCertificatesSHA256': pinnedCertificatesSHA256,
    };
  }

  factory SecurityConfig.fromMap(Map<String, dynamic> map) {
    return SecurityConfig(
      runtimeProtectionEnabled: map['runtimeProtectionEnabled'] as bool? ?? true,
      rootDetectionEnabled: map['rootDetectionEnabled'] as bool? ?? true,
      jailbreakDetectionEnabled: map['jailbreakDetectionEnabled'] as bool? ?? true,
      emulatorDetectionEnabled: map['emulatorDetectionEnabled'] as bool? ?? true,
      debuggerDetectionEnabled: map['debuggerDetectionEnabled'] as bool? ?? true,
      fridaDetectionEnabled: map['fridaDetectionEnabled'] as bool? ?? true,
      integrityCheckEnabled: map['integrityCheckEnabled'] as bool? ?? true,
      certificatePinningEnabled: map['certificatePinningEnabled'] as bool? ?? false,
      biometricEnabled: map['biometricEnabled'] as bool? ?? true,
      securityEventReportingEnabled:
          map['securityEventReportingEnabled'] as bool? ?? true,
      riskThreshold: map['riskThreshold'] as String? ?? 'MEDIUM',
      sessionTimeoutSeconds: map['sessionTimeoutSeconds'] as int? ?? 900,
      pinnedCertificatesSHA256:
          List<String>.from(map['pinnedCertificatesSHA256'] as List? ?? []),
    );
  }

  String toJson() => jsonEncode(toMap());

  factory SecurityConfig.fromJson(String source) =>
      SecurityConfig.fromMap(jsonDecode(source) as Map<String, dynamic>);
}
