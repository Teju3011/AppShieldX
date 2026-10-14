/// Constants defining API routes, gateway defaults, and timeouts.
class ApiConstants {
  ApiConstants._();

  // Gateway Base URL (Configurable via --dart-define=API_URL=http://<IP>:8080)
  static const String defaultBaseUrl = String.fromEnvironment(
    'API_URL',
    defaultValue: 'http://10.0.2.2:8080',
  );
  static const String iosSimulatorBaseUrl = String.fromEnvironment(
    'API_URL',
    defaultValue: 'http://localhost:8080',
  );

  // Network Timeouts
  static const Duration connectTimeout = Duration(seconds: 10);
  static const Duration receiveTimeout = Duration(seconds: 10);
  static const Duration sendTimeout = Duration(seconds: 10);

  // Authentication Endpoints
  static const String registerEndpoint = '/api/auth/register';
  static const String loginEndpoint = '/api/auth/login';
  static const String refreshEndpoint = '/api/auth/refresh';
  static const String logoutEndpoint = '/api/auth/logout';

  // User Endpoints
  static const String userMeEndpoint = '/api/users/me';
  static const String changePasswordEndpoint = '/api/users/change-password';

  // Business Endpoints
  static const String businessRecordsEndpoint = '/api/business/records';

  // Security Telemetry Endpoints
  static const String securityEventsEndpoint = '/api/security/events';
  static const String securityStatusEndpoint = '/api/security/status';

  // Administrative Endpoints
  static const String adminStatsEndpoint = '/api/admin/dashboard/stats';
  static const String adminSecurityEventsEndpoint = '/api/admin/security-events';
}
