import 'dart:io' show Platform;
import 'package:flutter/foundation.dart' show kIsWeb;
import '../constants/api_constants.dart';

/// Global application configuration and environment context.
class AppConfig {
  final String apiBaseUrl;
  final bool enableDebugLogs;
  final String environmentName;

  const AppConfig({
    required this.apiBaseUrl,
    this.enableDebugLogs = true,
    this.environmentName = 'development',
  });

  /// Factory creating development configuration targeting local gateway.
  factory AppConfig.development({String? customBaseUrl}) {
    if (customBaseUrl != null && customBaseUrl.isNotEmpty) {
      return AppConfig(
        apiBaseUrl: customBaseUrl,
        enableDebugLogs: true,
        environmentName: 'development',
      );
    }

    const envUrl = String.fromEnvironment('API_URL');
    if (envUrl.isNotEmpty) {
      return const AppConfig(
        apiBaseUrl: envUrl,
        enableDebugLogs: true,
        environmentName: 'development',
      );
    }

    String resolvedUrl = 'http://10.0.2.2:8080';
    if (kIsWeb) {
      final host = Uri.base.host.isNotEmpty ? Uri.base.host : 'localhost';
      resolvedUrl = 'http://$host:8080';
    } else {
      try {
        if (Platform.isIOS || Platform.isMacOS || Platform.isWindows || Platform.isLinux) {
          resolvedUrl = 'http://localhost:8080';
        } else if (Platform.isAndroid) {
          resolvedUrl = 'http://10.0.2.2:8080';
        }
      } catch (_) {
        resolvedUrl = 'http://localhost:8080';
      }
    }

    return AppConfig(
      apiBaseUrl: resolvedUrl,
      enableDebugLogs: true,
      environmentName: 'development',
    );
  }

  /// Factory creating production configuration.
  factory AppConfig.production({required String baseUrl}) {
    return AppConfig(
      apiBaseUrl: baseUrl,
      enableDebugLogs: false,
      environmentName: 'production',
    );
  }
}
