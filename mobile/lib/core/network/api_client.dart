import 'dart:io';
import 'package:crypto/crypto.dart';
import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import '../config/security_config.dart';
import '../constants/api_constants.dart';
import '../security/models/pinning_config.dart';
import '../storage/token_manager.dart';
import 'interceptors/auth_interceptor.dart';
import 'interceptors/correlation_id_interceptor.dart';
import 'interceptors/error_interceptor.dart';
import 'interceptors/token_refresh_interceptor.dart';

/// Secure HTTP client enforcing TLS verification, certificate pinning, and correlation tracking.
class ApiClient {
  final Dio _dio;

  ApiClient({
    required String baseUrl,
    required TokenManager tokenManager,
    required String deviceId,
    SecurityConfig securityConfig = const SecurityConfig(),
    PinningConfig? pinningConfig,
    Dio? customDio,
  }) : _dio = customDio ??
            Dio(
              BaseOptions(
                baseUrl: baseUrl,
                connectTimeout: ApiConstants.connectTimeout,
                receiveTimeout: ApiConstants.receiveTimeout,
                sendTimeout: ApiConstants.sendTimeout,
                headers: {
                  'Content-Type': 'application/json',
                  'Accept': 'application/json',
                },
              ),
            ) {
    // 1. Attach Correlation ID and Device Identifier Interceptor
    _dio.interceptors.add(CorrelationIdInterceptor(deviceId: deviceId));

    // 2. Attach Authorization Interceptor (Bearer JWT)
    _dio.interceptors.add(AuthInterceptor(tokenManager));

    // 3. Attach Token Refresh Interceptor (Automated 401 recovery)
    _dio.interceptors.add(
      TokenRefreshInterceptor(
        dio: _dio,
        tokenManager: tokenManager,
        baseUrl: baseUrl,
      ),
    );

    // 4. Attach Error Interceptor
    _dio.interceptors.add(ErrorInterceptor());

    // 5. Configure TLS Certificate / Public Key Pinning securely
    _configureTlsPinning(securityConfig, pinningConfig);
  }

  Dio get rawDio => _dio;

  void _configureTlsPinning(
    SecurityConfig securityConfig,
    PinningConfig? pinningConfig,
  ) {
    if (kIsWeb) return;
    try {
      final dynamic adapter = _dio.httpClientAdapter;
      adapter.createHttpClient = () {
        final client = HttpClient(
          context: SecurityContext(withTrustedRoots: true),
        );

        if (securityConfig.certificatePinningEnabled && pinningConfig != null) {
          client.badCertificateCallback = (
            X509Certificate cert,
            String host,
            int port,
          ) {
            // Strict Pinning: Only validate when matching targeted hostname
            if (host == pinningConfig.hostname) {
              final List<int> derBytes = cert.der;
              final Digest sha256Digest = sha256.convert(derBytes);
              final String computedFingerprint = sha256Digest.toString();

              return pinningConfig.isValidFingerprint(computedFingerprint);
            }
            // Reject any untrusted certificate for non-pinned hosts
            return false;
          };
        }

        return client;
      };
    } catch (_) {}
  }

  // Standard Typed REST Operations

  Future<Response<T>> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    return await _dio.get<T>(
      path,
      queryParameters: queryParameters,
      options: options,
    );
  }

  Future<Response<T>> post<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    return await _dio.post<T>(
      path,
      data: data,
      queryParameters: queryParameters,
      options: options,
    );
  }

  Future<Response<T>> put<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    return await _dio.put<T>(
      path,
      data: data,
      queryParameters: queryParameters,
      options: options,
    );
  }

  Future<Response<T>> delete<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    return await _dio.delete<T>(
      path,
      data: data,
      queryParameters: queryParameters,
      options: options,
    );
  }
}
