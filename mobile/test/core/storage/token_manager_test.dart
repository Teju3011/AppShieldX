import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_security_reference_app/core/security/providers/secure_storage_provider.dart';
import 'package:mobile_security_reference_app/core/storage/token_manager.dart';

class MockSecureStorageProvider implements SecureStorageProvider {
  final Map<String, String> _storage = {};

  @override
  Future<void> write(String key, String value) async {
    _storage[key] = value;
  }

  @override
  Future<String?> read(String key) async {
    return _storage[key];
  }

  @override
  Future<void> delete(String key) async {
    _storage.remove(key);
  }

  @override
  Future<bool> containsKey(String key) async {
    return _storage.containsKey(key);
  }

  @override
  Future<void> clearAll() async {
    _storage.clear();
  }
}

void main() {
  group('TokenManager Lifecycle Tests', () {
    late MockSecureStorageProvider mockStorage;
    late TokenManager tokenManager;

    setUp(() {
      mockStorage = MockSecureStorageProvider();
      tokenManager = TokenManager(mockStorage);
    });

    test('Initial session state reports invalid session', () async {
      final isValid = await tokenManager.hasValidSession();
      expect(isValid, isFalse);
    });

    test('saveTokens commits access and refresh tokens into secure storage', () async {
      await tokenManager.saveTokens(
        accessToken: 'mock_access_jwt',
        refreshToken: 'mock_refresh_token',
      );

      expect(await tokenManager.getAccessToken(), equals('mock_access_jwt'));
      expect(await tokenManager.getRefreshToken(), equals('mock_refresh_token'));
      expect(await tokenManager.hasValidSession(), isTrue);
    });

    test('saveUserSession serializes roles and retrieves correctly', () async {
      await tokenManager.saveUserSession(
        userId: 'user-12345',
        roles: ['ROLE_USER', 'ROLE_ADMIN'],
      );

      expect(await tokenManager.getUserId(), equals('user-12345'));
      final roles = await tokenManager.getUserRoles();
      expect(roles, containsAll(['ROLE_USER', 'ROLE_ADMIN']));
    });

    test('clearSession purges all sensitive credentials', () async {
      await tokenManager.saveTokens(
        accessToken: 'mock_jwt',
        refreshToken: 'mock_refresh',
      );
      await tokenManager.saveUserSession(
        userId: 'user-123',
        roles: ['ROLE_USER'],
      );

      await tokenManager.clearSession();

      expect(await tokenManager.getAccessToken(), isNull);
      expect(await tokenManager.getRefreshToken(), isNull);
      expect(await tokenManager.getUserId(), isNull);
      expect(await tokenManager.getUserRoles(), isEmpty);
      expect(await tokenManager.hasValidSession(), isFalse);
    });
  });
}
