import '../../constants/security_constants.dart';
import '../models/risk_level.dart';
import '../models/security_status.dart';

/// Evaluates runtime security diagnostic indicators and computes categorical risk levels.
class RiskEvaluationProvider {
  const RiskEvaluationProvider();

  /// Evaluates an aggregated list of detected threat strings.
  RiskLevel evaluateThreats(List<String> threats) {
    if (threats.isEmpty) {
      return RiskLevel.low;
    }

    // Critical severity indicators (Immediate session invalidation)
    final bool hasCriticalThreat = threats.any((threat) =>
        threat == SecurityConstants.eventRootDetected ||
        threat == SecurityConstants.eventJailbreakDetected ||
        threat == SecurityConstants.eventFridaDetected ||
        threat == SecurityConstants.eventTamperingDetected ||
        threat == SecurityConstants.eventIntegrityFailure);

    if (hasCriticalThreat) {
      return RiskLevel.critical;
    }

    // High severity indicators (Dynamic reverse-engineering tools)
    final bool hasHighThreat = threats.any(
      (threat) => threat == SecurityConstants.eventDebuggerDetected,
    );

    if (hasHighThreat) {
      // Multiple high/medium threats escalate to critical
      if (threats.length >= 2) {
        return RiskLevel.critical;
      }
      return RiskLevel.high;
    }

    // Medium severity indicators (Emulators, virtual environments)
    final bool hasMediumThreat = threats.any((threat) =>
        threat == SecurityConstants.eventEmulatorDetected ||
        threat == SecurityConstants.eventSimulatorDetected ||
        threat == SecurityConstants.eventRateLimitExceeded);

    if (hasMediumThreat) {
      if (threats.length >= 3) {
        return RiskLevel.high;
      }
      return RiskLevel.medium;
    }

    return RiskLevel.low;
  }

  /// Evaluates a full [SecurityStatus] snapshot.
  RiskLevel evaluateStatus(SecurityStatus status) {
    return evaluateThreats(status.detectedThreats);
  }
}
