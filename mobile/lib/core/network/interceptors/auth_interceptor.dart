import 'package:dio/dio.dart';
import '../../constants/api_constants.dart';
import '../../constants/security_constants.dart';
import '../../storage/token_manager.dart';

/// Interceptor attaching cryptographically signed JWT Bearer tokens to authenticated requests.
class AuthInterceptor extends Interceptor {
  final TokenManager _tokenManager;

  AuthInterceptor(this._tokenManager);

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    // Skip authorization header for anonymous authentication endpoints
    final String path = options.path;
    final bool isAuthEndpoint = path.contains(ApiConstants.loginEndpoint) ||
        path.contains(ApiConstants.registerEndpoint) ||
        path.contains(ApiConstants.refreshEndpoint);

    if (!isAuthEndpoint) {
      final String? token = await _tokenManager.getAccessToken();
      if (token != null && token.isNotEmpty) {
        options.headers[SecurityConstants.authorizationHeader] =
            '${SecurityConstants.bearerPrefix}$token';
      }
    }

    handler.next(options);
  }
}
