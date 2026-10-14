import '../../../../core/constants/api_constants.dart';
import '../../../../core/error/exceptions.dart';
import '../../../../core/network/api_client.dart';
import '../../../../core/storage/token_manager.dart';
import '../../domain/repositories/auth_repository.dart';
import '../models/user_model.dart';

/// Concrete implementation of [AuthRepository] interacting with API Gateway endpoints.
class AuthRepositoryImpl implements AuthRepository {
  final ApiClient _apiClient;
  final TokenManager _tokenManager;

  AuthRepositoryImpl({
    required ApiClient apiClient,
    required TokenManager tokenManager,
  })  : _apiClient = apiClient,
        _tokenManager = tokenManager;

  @override
  Future<UserModel> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await _apiClient.post(
        ApiConstants.loginEndpoint,
        data: {
          'email': email.trim(),
          'password': password,
        },
      );

      if (response.statusCode == 200 && response.data != null) {
        final Map<String, dynamic> data =
            Map<String, dynamic>.from(response.data as Map);
        final String accessToken = data['accessToken'] as String;
        final String refreshToken = data['refreshToken'] as String;
        final Map<String, dynamic> userMap =
            Map<String, dynamic>.from(data['user'] as Map);

        final user = UserModel.fromMap(userMap);

        // Commit newly issued tokens and session state to hardware keystore
        await _tokenManager.saveTokens(
          accessToken: accessToken,
          refreshToken: refreshToken,
        );
        await _tokenManager.saveUserSession(
          userId: user.id,
          roles: user.roles,
        );

        return user;
      } else {
        throw const AuthenticationException('Invalid response received from server');
      }
    } on SecurityException {
      rethrow;
    } catch (e) {
      throw AuthenticationException('Authentication request failed: $e');
    }
  }

  @override
  Future<void> register({
    required String username,
    required String email,
    required String password,
  }) async {
    try {
      await _apiClient.post(
        ApiConstants.registerEndpoint,
        data: {
          'username': username.trim(),
          'email': email.trim(),
          'password': password,
        },
      );
    } on SecurityException {
      rethrow;
    } catch (e) {
      throw AuthenticationException('Registration request failed: $e');
    }
  }

  @override
  Future<void> logout() async {
    try {
      await _apiClient.post(ApiConstants.logoutEndpoint);
    } catch (_) {
      // Proceed with local wipe even if server call fails
    } finally {
      await _tokenManager.clearSession();
    }
  }

  @override
  Future<UserModel?> getCurrentUser() async {
    final bool hasSession = await _tokenManager.hasValidSession();
    if (!hasSession) return null;

    try {
      final response = await _apiClient.get(ApiConstants.userMeEndpoint);
      if (response.statusCode == 200 && response.data != null) {
        final Map<String, dynamic> data =
            Map<String, dynamic>.from(response.data as Map);
        return UserModel.fromMap(data);
      }
    } catch (_) {
      // Session invalid or gateway unreachable
    }
    return null;
  }

  @override
  Future<bool> isAuthenticated() async {
    return await _tokenManager.hasValidSession();
  }
}
