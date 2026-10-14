/// Core domain exception hierarchy for the security framework.

class SecurityException implements Exception {
  final String message;
  final String? code;
  final dynamic details;

  const SecurityException(this.message, {this.code, this.details});

  @override
  String toString() => 'SecurityException: $message (code: $code)';
}

class RuntimeThreatDetectedException extends SecurityException {
  final List<String> threats;
  final String riskLevel;

  const RuntimeThreatDetectedException({
    required this.threats,
    required this.riskLevel,
    String message = 'Host environment compromised by active security threats',
  }) : super(message, code: 'RUNTIME_THREAT_DETECTED', details: threats);
}

class SecureStorageException extends SecurityException {
  const SecureStorageException(super.message, {super.code, super.details});
}

class NetworkSecurityException extends SecurityException {
  final int? statusCode;
  final String? correlationId;

  const NetworkSecurityException(
    super.message, {
    super.code,
    this.statusCode,
    this.correlationId,
    super.details,
  });
}

class AuthenticationException extends SecurityException {
  const AuthenticationException(super.message, {super.code = 'AUTH_ERROR'});
}

class RateLimitExceededException extends NetworkSecurityException {
  final int retryAfterSeconds;

  const RateLimitExceededException({
    String message = 'Rate limit exceeded. Please throttle requests.',
    this.retryAfterSeconds = 60,
    String? correlationId,
  }) : super(message, code: 'RATE_LIMIT_EXCEEDED', statusCode: 429, correlationId: correlationId);
}

class CertificatePinningException extends NetworkSecurityException {
  const CertificatePinningException([
    super.message = 'TLS certificate or public key verification failure',
  ]) : super(code: 'CERTIFICATE_PINNING_FAILED');
}
