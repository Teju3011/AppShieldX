/// Risk classification levels with associated behavioral policies.
enum RiskLevel {
  low,
  medium,
  high,
  critical;

  /// Parse string representation to enum safely.
  static RiskLevel fromString(String? value) {
    if (value == null) return RiskLevel.low;
    switch (value.toUpperCase()) {
      case 'CRITICAL':
        return RiskLevel.critical;
      case 'HIGH':
        return RiskLevel.high;
      case 'MEDIUM':
        return RiskLevel.medium;
      case 'LOW':
      default:
        return RiskLevel.low;
    }
  }

  /// Convert enum to upper-case protocol string.
  String toProtocolString() {
    switch (this) {
      case RiskLevel.critical:
        return 'CRITICAL';
      case RiskLevel.high:
        return 'HIGH';
      case RiskLevel.medium:
        return 'MEDIUM';
      case RiskLevel.low:
        return 'LOW';
    }
  }

  /// Whether current risk mandates immediate application termination or session wipe.
  bool get shouldTerminateSession => this == RiskLevel.critical;

  /// Whether current risk restricts sensitive transactional operations.
  bool get shouldRestrictOperations =>
      this == RiskLevel.high || this == RiskLevel.critical;

  /// Numerical score equivalent for telemetry aggregation.
  int get numericalScore {
    switch (this) {
      case RiskLevel.critical:
        return 90;
      case RiskLevel.high:
        return 70;
      case RiskLevel.medium:
        return 40;
      case RiskLevel.low:
        return 10;
    }
  }
}
