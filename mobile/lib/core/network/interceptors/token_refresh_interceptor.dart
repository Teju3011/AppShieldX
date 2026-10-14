import 'dart:async';
import 'package:dio/dio.dart';
import '../../constants/api_constants.dart';
import '../../constants/security_constants.dart';
import '../../storage/token_manager.dart';

/// Interceptor intercepting 401 Unauthorized responses to perform automatic transparent token refresh.
class TokenRefreshInterceptor extends QueuedInterceptor {
  final Dio _dio;
  final TokenManager _tokenManager;
  final String _baseUrl;
  bool _isRefreshing = false;

  TokenRefreshInterceptor({
    required Dio dio,
    required TokenManager tokenManager,
    required String baseUrl,
  })  : _dio = dio,
        _tokenManager = tokenManager,
        _baseUrl = baseUrl;

  @override
  Future<void> onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    final RequestOptions requestOptions = err.requestOptions;

    // Check if error is 401 Unauthorized and not an auth endpoint itself
    final bool isUnauthorized = err.response?.statusCode == 401;
    final bool isAuthEndpoint =
        requestOptions.path.contains(ApiConstants.loginEndpoint) ||
            requestOptions.path.contains(ApiConstants.refreshEndpoint) ||
            requestOptions.path.contains(ApiConstants.registerEndpoint);

    if (!isUnauthorized || isAuthEndpoint || _isRefreshing) {
      return handler.next(err);
    }

    _isRefreshing = true;

    try {
      final String? currentRefreshToken =
          await _tokenManager.getRefreshToken();
      if (currentRefreshToken == null || currentRefreshToken.isEmpty) {
        await _tokenManager.clearSession();
        return handler.next(err);
      }

      // Use a distinct isolated Dio client to prevent recursion
      final Dio refreshDio = Dio(
        BaseOptions(
          baseUrl: _baseUrl,
          connectTimeout: ApiConstants.connectTimeout,
          receiveTimeout: ApiConstants.receiveTimeout,
        ),
      );

      final Response<dynamic> refreshResponse = await refreshDio.post(
        ApiConstants.refreshEndpoint,
        data: {'refreshToken': currentRefreshToken},
      );

      if (refreshResponse.statusCode == 200 && refreshResponse.data != null) {
        final Map<String, dynamic> data =
            Map<String, dynamic>.from(refreshResponse.data as Map);
        final String newAccessToken = data['accessToken'] as String;
        final String newRefreshToken =
            data['refreshToken'] as String? ?? currentRefreshToken;

        // Persist newly rotated credentials
        await _tokenManager.saveTokens(
          accessToken: newAccessToken,
          refreshToken: newRefreshToken,
        );

        // Update authorization header and replay original request
        requestOptions.headers[SecurityConstants.authorizationHeader] =
            '${SecurityConstants.bearerPrefix}$newAccessToken';

        final Response<dynamic> retryResponse =
            await _dio.fetch<dynamic>(requestOptions);
        return handler.resolve(retryResponse);
      } else {
        await _tokenManager.clearSession();
        return handler.next(err);
      }
    } catch (_) {
      await _tokenManager.clearSession();
      return handler.next(err);
    } finally {
      _isRefreshing = false;
    }
  }
}
