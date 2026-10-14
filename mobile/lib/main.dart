import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/config/app_config.dart';
import 'core/config/security_config.dart';
import 'core/security/security_framework.dart';
import 'features/auth/data/repositories/auth_repository_impl.dart';
import 'features/auth/presentation/providers/auth_provider.dart';
import 'features/security/data/repositories/security_repository_impl.dart';
import 'features/security/presentation/providers/security_provider.dart';
import 'core/network/api_client.dart';
import 'core/security/providers/flutter_secure_storage_provider.dart';
import 'core/storage/token_manager.dart';
import 'routing/app_router.dart';
import 'theme/app_theme.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // 1. Initialize Application Environment Configuration
  final appConfig = AppConfig.development();

  // 2. Initialize the Reusable Mobile Security Framework
  SecurityFramework? securityFramework;
  try {
    securityFramework = await SecurityFramework.initialize(
      config: SecurityConfig.development(),
      apiBaseUrl: appConfig.apiBaseUrl,
    );
  } catch (e, stack) {
    debugPrint('AppShieldX: SecurityFramework init exception: $e\n$stack');
  }

  // 3. Create Authenticated API Client
  final tokenManager = securityFramework?.tokenManager ??
      TokenManager(FlutterSecureStorageProvider());

  final apiClient = securityFramework != null
      ? securityFramework.createSecureApiClient(
          baseUrl: appConfig.apiBaseUrl,
        )
      : ApiClient(
          baseUrl: appConfig.apiBaseUrl,
          tokenManager: tokenManager,
          deviceId: 'ios-web-client',
        );

  // 4. Instantiate Repository Layers
  final authRepository = AuthRepositoryImpl(
    apiClient: apiClient,
    tokenManager: tokenManager,
  );

  final securityRepository = securityFramework != null
      ? SecurityRepositoryImpl(framework: securityFramework)
      : null;

  runApp(
    ProviderScope(
      overrides: [
        authRepositoryProvider.overrideWithValue(authRepository),
        if (securityRepository != null)
          securityRepositoryProvider.overrideWithValue(securityRepository),
      ],
      child: const SecureApp(),
    ),
  );
}

/// Root widget for the reference mobile application.
class SecureApp extends ConsumerWidget {
  const SecureApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(appRouterProvider);

    return MaterialApp.router(
      title: 'AppShieldX - Mobile Security Framework',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.darkTheme,
      routerConfig: router,
    );
  }
}
