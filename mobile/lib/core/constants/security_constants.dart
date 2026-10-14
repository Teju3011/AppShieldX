/// Security framework constants defining channel names, headers, storage keys, and event types.
class SecurityConstants {
  SecurityConstants._();

  // MethodChannel Name for Native RASP Bridges
  static const String runtimeProtectionChannel =
      'com.framework.security/runtime_protection';

  // HTTP Header Keys
  static const String correlationIdHeader = 'X-Correlation-ID';
  static const String deviceIdHeader = 'X-Device-ID';
  static const String authorizationHeader = 'Authorization';
  static const String bearerPrefix = 'Bearer ';

  // Secure Storage Keys
  static const String storageAccessTokenKey = 'sec_access_token';
  static const String storageRefreshTokenKey = 'sec_refresh_token';
  static const String storageDeviceIdKey = 'sec_device_id';
  static const String storageUserIdKey = 'sec_user_id';
  static const String storageUserRolesKey = 'sec_user_roles';
  static const String storageSecurityConfigKey = 'sec_security_config';

  // Security Event Types
  static const String eventRootDetected = 'ROOT_DETECTED';
  static const String eventJailbreakDetected = 'JAILBREAK_DETECTED';
  static const String eventEmulatorDetected = 'EMULATOR_DETECTED';
  static const String eventSimulatorDetected = 'SIMULATOR_DETECTED';
  static const String eventDebuggerDetected = 'DEBUGGER_DETECTED';
  static const String eventFridaDetected = 'FRIDA_DETECTED';
  static const String eventTamperingDetected = 'TAMPERING_DETECTED';
  static const String eventIntegrityFailure = 'INTEGRITY_FAILURE';
  static const String eventAuthFailure = 'AUTH_FAILURE';
  static const String eventRateLimitExceeded = 'RATE_LIMIT_EXCEEDED';
  static const String eventSuspiciousApiRequest = 'SUSPICIOUS_API_REQUEST';
  static const String eventPolicyViolation = 'POLICY_VIOLATION';

  // Risk Levels
  static const String riskLow = 'LOW';
  static const String riskMedium = 'MEDIUM';
  static const String riskHigh = 'HIGH';
  static const String riskCritical = 'CRITICAL';

  // Default Offline Queue Parameters
  static const int maxOfflineEvents = 1000;
  static const int batchUploadSize = 25;
}
