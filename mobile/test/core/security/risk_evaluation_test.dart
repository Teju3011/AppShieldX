import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_security_reference_app/core/constants/security_constants.dart';
import 'package:mobile_security_reference_app/core/security/models/risk_level.dart';
import 'package:mobile_security_reference_app/core/security/providers/risk_evaluation_provider.dart';

void main() {
  group('RiskEvaluationProvider Engine Tests', () {
    const evaluator = RiskEvaluationProvider();

    test('Empty threat list returns LOW risk level', () {
      final risk = evaluator.evaluateThreats([]);
      expect(risk, equals(RiskLevel.low));
      expect(risk.shouldTerminateSession, isFalse);
      expect(risk.shouldRestrictOperations, isFalse);
    });

    test('Emulator or Simulator alone returns MEDIUM risk level', () {
      final risk = evaluator.evaluateThreats([SecurityConstants.eventEmulatorDetected]);
      expect(risk, equals(RiskLevel.medium));
      expect(risk.shouldTerminateSession, isFalse);
      expect(risk.shouldRestrictOperations, isFalse);
    });

    test('Debugger detection alone returns HIGH risk level', () {
      final risk = evaluator.evaluateThreats([SecurityConstants.eventDebuggerDetected]);
      expect(risk, equals(RiskLevel.high));
      expect(risk.shouldTerminateSession, isFalse);
      expect(risk.shouldRestrictOperations, isTrue);
    });

    test('Frida or Root detection immediately triggers CRITICAL risk level', () {
      final fridaRisk = evaluator.evaluateThreats([SecurityConstants.eventFridaDetected]);
      expect(fridaRisk, equals(RiskLevel.critical));
      expect(fridaRisk.shouldTerminateSession, isTrue);

      final rootRisk = evaluator.evaluateThreats([SecurityConstants.eventRootDetected]);
      expect(rootRisk, equals(RiskLevel.critical));
      expect(rootRisk.shouldTerminateSession, isTrue);
    });

    test('Multiple concurrent threats escalate risk to CRITICAL', () {
      final multiRisk = evaluator.evaluateThreats([
        SecurityConstants.eventDebuggerDetected,
        SecurityConstants.eventEmulatorDetected,
      ]);
      expect(multiRisk, equals(RiskLevel.critical));
    });
  });
}
