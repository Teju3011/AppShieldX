import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_security_reference_app/core/constants/security_constants.dart';
import 'package:mobile_security_reference_app/core/security/models/risk_level.dart';
import 'package:mobile_security_reference_app/core/security/providers/risk_evaluation_provider.dart';

void main() {
  test('AppShieldX Mobile Security Framework Smoke Test', () {
    const evaluator = RiskEvaluationProvider();
    final risk = evaluator.evaluateThreats([]);
    expect(risk, equals(RiskLevel.low));
    expect(risk.shouldTerminateSession, isFalse);
  });
}
