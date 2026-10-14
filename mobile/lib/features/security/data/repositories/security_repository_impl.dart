import '../../../../core/constants/security_constants.dart';
import '../../../../core/security/models/security_event.dart';
import '../../../../core/security/models/security_status.dart';
import '../../../../core/security/providers/risk_evaluation_provider.dart';
import '../../../../core/security/security_framework.dart';
import '../../domain/repositories/security_repository.dart';

/// Concrete implementation of [SecurityRepository] powered by the [SecurityFramework].
class SecurityRepositoryImpl implements SecurityRepository {
  final SecurityFramework _framework;
  final RiskEvaluationProvider _riskEvaluator;

  SecurityRepositoryImpl({
    required SecurityFramework framework,
    RiskEvaluationProvider? riskEvaluator,
  })  : _framework = framework,
        _riskEvaluator = riskEvaluator ?? const RiskEvaluationProvider();

  @override
  Future<SecurityStatus> runSecurityAudit() async {
    return await _framework.checkRuntimeSecurity();
  }

  @override
  Future<SecurityStatus> getLastStatus() async {
    return await _framework.getSecurityStatus();
  }

  @override
  Future<void> reportEvent(SecurityEvent event) async {
    await _framework.reportSecurityEvent(event);
  }

  @override
  Future<SecurityStatus> simulateThreat(String threatType) async {
    final currentStatus = await _framework.getSecurityStatus();
    final updatedThreats = List<String>.from(currentStatus.detectedThreats);

    if (!updatedThreats.contains(threatType)) {
      updatedThreats.add(threatType);
    }

    final newRisk = _riskEvaluator.evaluateThreats(updatedThreats);

    final simulatedStatus = currentStatus.copyWith(
      rootDetected: threatType == SecurityConstants.eventRootDetected ||
          currentStatus.rootDetected,
      jailbreakDetected: threatType == SecurityConstants.eventJailbreakDetected ||
          currentStatus.jailbreakDetected,
      emulatorDetected: threatType == SecurityConstants.eventEmulatorDetected ||
          currentStatus.emulatorDetected,
      simulatorDetected: threatType == SecurityConstants.eventSimulatorDetected ||
          currentStatus.simulatorDetected,
      debuggerDetected: threatType == SecurityConstants.eventDebuggerDetected ||
          currentStatus.debuggerDetected,
      fridaDetected: threatType == SecurityConstants.eventFridaDetected ||
          currentStatus.fridaDetected,
      integrityValid: threatType != SecurityConstants.eventIntegrityFailure &&
          currentStatus.integrityValid,
      riskLevel: newRisk,
      detectedThreats: updatedThreats,
      timestamp: DateTime.now().toUtc(),
    );

    // Stream telemetry alert to backend
    await _framework.reportThreatDetected(
      eventType: threatType,
      severity: newRisk.toProtocolString(),
      description: 'DEMONSTRATION: Simulated threat triggered ($threatType)',
      metadata: {'simulated': true, 'riskLevel': newRisk.toProtocolString()},
    );

    return simulatedStatus;
  }

  @override
  Future<int> flushPendingEvents() async {
    return await _framework.eventReporter.flushQueue();
  }

  @override
  Future<int> getOfflineQueueCount() async {
    return await _framework.eventReporter.getPendingQueueCount();
  }
}
