import '../../data/models/user_model.dart';

/// Abstract repository defining authentication actions and session verification.
abstract class AuthRepository {
  /// Authenticates credentials against the backend API Gateway.
  Future<UserModel> login({
    required String email,
    required String password,
  });

  /// Registers a new user account.
  Future<void> register({
    required String username,
    required String email,
    required String password,
  });

  /// Terminates active session on device and backend.
  Future<void> logout();

  /// Retrieves cached user session if access token exists.
  Future<UserModel?> getCurrentUser();

  /// Checks if device has an authenticated session.
  Future<bool> isAuthenticated();
}
