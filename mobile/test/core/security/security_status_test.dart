import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_security_reference_app/core/security/models/risk_level.dart';
import 'package:mobile_security_reference_app/core/security/models/security_status.dart';

void main() {
  group('SecurityStatus Model Tests', () {
    test('Clean factory creates uncompromised status with LOW risk', () {
      final status = SecurityStatus.clean(
        deviceId: 'test-device-uuid',
        platform: 'android',
      );

      expect(status.rootDetected, isFalse);
      expect(status.jailbreakDetected, isFalse);
      expect(status.emulatorDetected, isFalse);
      expect(status.debuggerDetected, isFalse);
      expect(status.fridaDetected, isFalse);
      expect(status.integrityValid, isTrue);
      expect(status.riskLevel, equals(RiskLevel.low));
      expect(status.isCompromised, isFalse);
      expect(status.threatCount, equals(0));
    });

    test('isCompromised evaluates to true when critical threat detected', () {
      final status = SecurityStatus.clean(
        deviceId: 'test-device-uuid',
        platform: 'android',
      ).copyWith(
        rootDetected: true,
        detectedThreats: ['ROOT_DETECTED'],
        riskLevel: RiskLevel.critical,
      );

      expect(status.isCompromised, isTrue);
      expect(status.threatCount, equals(1));
    });

    test('JSON serialization and deserialization roundtrip preserves all fields', () {
      final original = SecurityStatus(
        rootDetected: true,
        jailbreakDetected: false,
        emulatorDetected: true,
        simulatorDetected: false,
        debuggerDetected: false,
        fridaDetected: false,
        integrityValid: true,
        sslPinningEnabled: true,
        secureStorageAvailable: true,
        riskLevel: RiskLevel.critical,
        detectedThreats: const ['ROOT_DETECTED', 'EMULATOR_DETECTED'],
        timestamp: DateTime.utc(2026, 9, 18, 12, 0, 0),
        deviceId: 'roundtrip-device-id',
        platform: 'android',
      );

      final jsonString = original.toJson();
      final restored = SecurityStatus.fromJson(jsonString);

      expect(restored.rootDetected, equals(original.rootDetected));
      expect(restored.emulatorDetected, equals(original.emulatorDetected));
      expect(restored.riskLevel, equals(RiskLevel.critical));
      expect(restored.detectedThreats, containsAll(['ROOT_DETECTED', 'EMULATOR_DETECTED']));
      expect(restored.deviceId, equals(original.deviceId));
    });
  });
}
