import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_security_reference_app/features/auth/data/models/user_model.dart';
import 'package:mobile_security_reference_app/features/auth/domain/repositories/auth_repository.dart';
import 'package:mobile_security_reference_app/features/auth/presentation/providers/auth_provider.dart';

class MockAuthRepository implements AuthRepository {
  UserModel? mockUser;
  bool shouldFail = false;

  @override
  Future<UserModel> login({required String email, required String password}) async {
    if (shouldFail) throw Exception('Invalid credentials');
    mockUser = UserModel(
      id: 'mock-uuid',
      username: 'alice',
      email: email,
      roles: ['ROLE_USER'],
    );
    return mockUser!;
  }

  @override
  Future<void> register({
    required String username,
    required String email,
    required String password,
  }) async {
    if (shouldFail) throw Exception('Email already in use');
  }

  @override
  Future<void> logout() async {
    mockUser = null;
  }

  @override
  Future<UserModel?> getCurrentUser() async {
    return mockUser;
  }

  @override
  Future<bool> isAuthenticated() async {
    return mockUser != null;
  }
}

void main() {
  group('AuthNotifier State Tests', () {
    late MockAuthRepository mockRepo;
    late AuthNotifier notifier;

    setUp(() {
      mockRepo = MockAuthRepository();
      notifier = AuthNotifier(mockRepo);
    });

    test('Initial state is unauthenticated without user', () {
      expect(notifier.state.isAuthenticated, isFalse);
      expect(notifier.state.user, isNull);
    });

    test('login updates state to authenticated on success', () async {
      final success = await notifier.login(
        email: 'alice@securityframework.io',
        password: 'ValidPassword123!',
      );

      expect(success, isTrue);
      expect(notifier.state.isAuthenticated, isTrue);
      expect(notifier.state.user?.username, equals('alice'));
      expect(notifier.state.errorMessage, isNull);
    });

    test('login sets error message on failure', () async {
      mockRepo.shouldFail = true;

      final success = await notifier.login(
        email: 'attacker@bad.io',
        password: 'WrongPassword',
      );

      expect(success, isFalse);
      expect(notifier.state.isAuthenticated, isFalse);
      expect(notifier.state.errorMessage, isNotNull);
    });

    test('logout resets authentication state', () async {
      await notifier.login(
        email: 'alice@securityframework.io',
        password: 'Password123!',
      );
      expect(notifier.state.isAuthenticated, isTrue);

      await notifier.logout();
      expect(notifier.state.isAuthenticated, isFalse);
      expect(notifier.state.user, isNull);
    });
  });
}
