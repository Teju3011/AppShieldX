import 'dart:convert';
import '../constants/security_constants.dart';
import '../security/providers/secure_storage_provider.dart';

/// Manages secure persistence and lifecycle of access tokens, refresh tokens, and user credentials.
class TokenManager {
  final SecureStorageProvider _storage;

  TokenManager(this._storage);

  /// Commits newly issued access and refresh tokens to hardware-backed storage.
  Future<void> saveTokens({
    required String accessToken,
    required String refreshToken,
  }) async {
    await _storage.write(SecurityConstants.storageAccessTokenKey, accessToken);
    await _storage.write(
        SecurityConstants.storageRefreshTokenKey, refreshToken);
  }

  /// Retrieves the cached access token (JWT).
  Future<String?> getAccessToken() async {
    return await _storage.read(SecurityConstants.storageAccessTokenKey);
  }

  /// Retrieves the long-lived refresh token.
  Future<String?> getRefreshToken() async {
    return await _storage.read(SecurityConstants.storageRefreshTokenKey);
  }

  /// Persists user identity and assigned RBAC roles.
  Future<void> saveUserSession({
    required String userId,
    required List<String> roles,
  }) async {
    await _storage.write(SecurityConstants.storageUserIdKey, userId);
    await _storage.write(
        SecurityConstants.storageUserRolesKey, jsonEncode(roles));
  }

  /// Retrieves the active user ID.
  Future<String?> getUserId() async {
    return await _storage.read(SecurityConstants.storageUserIdKey);
  }

  /// Retrieves the list of user roles.
  Future<List<String>> getUserRoles() async {
    final String? rolesJson =
        await _storage.read(SecurityConstants.storageUserRolesKey);
    if (rolesJson == null) return const [];
    try {
      final List<dynamic> decoded = jsonDecode(rolesJson) as List<dynamic>;
      return decoded.map((e) => e.toString()).toList();
    } catch (_) {
      return const [];
    }
  }

  /// Queries whether an authenticated session exists.
  Future<bool> hasValidSession() async {
    final String? token = await getAccessToken();
    return token != null && token.isNotEmpty;
  }

  /// Wipes all cached tokens and session state from keystore.
  Future<void> clearSession() async {
    await _storage.delete(SecurityConstants.storageAccessTokenKey);
    await _storage.delete(SecurityConstants.storageRefreshTokenKey);
    await _storage.delete(SecurityConstants.storageUserIdKey);
    await _storage.delete(SecurityConstants.storageUserRolesKey);
  }
}
