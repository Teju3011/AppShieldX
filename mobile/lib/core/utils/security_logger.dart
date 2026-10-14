import 'dart:developer' as developer;

/// Security-conscious logger ensuring credentials and tokens are scrubbed from console output.
class SecurityLogger {
  final bool enableDebugLogs;

  const SecurityLogger({this.enableDebugLogs = true});

  void info(String message, {String? tag}) {
    if (!enableDebugLogs) return;
    developer.log(
      _sanitize(message),
      name: tag ?? 'SecurityFramework',
      level: 800,
    );
  }

  void warn(String message, {String? tag, dynamic error}) {
    developer.log(
      '⚠️ ${_sanitize(message)}',
      name: tag ?? 'SecurityFramework',
      error: error,
      level: 900,
    );
  }

  void error(String message, {String? tag, dynamic error, StackTrace? stack}) {
    developer.log(
      '🛑 ${_sanitize(message)}',
      name: tag ?? 'SecurityFramework',
      error: error,
      stackTrace: stack,
      level: 1000,
    );
  }

  /// Scrubs sensitive tokens, passwords, and authorization headers from strings.
  String _sanitize(String input) {
    return input
        .replaceAll(RegExp(r'Bearer\s+[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+\.?[A-Za-z0-9\-_=]*'), 'Bearer [REDACTED_JWT]')
        .replaceAll(RegExp(r'"password":\s*"[^"]+"'), '"password": "[REDACTED]"')
        .replaceAll(RegExp(r'"refreshToken":\s*"[^"]+"'), '"refreshToken": "[REDACTED]"')
        .replaceAll(RegExp(r'"accessToken":\s*"[^"]+"'), '"accessToken": "[REDACTED]"');
  }
}
