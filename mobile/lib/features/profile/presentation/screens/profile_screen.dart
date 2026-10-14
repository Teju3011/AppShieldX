import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../theme/app_theme.dart';
import '../../../auth/presentation/providers/auth_provider.dart';

/// User profile screen presenting authenticated identity, roles, and sign-out controls.
class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authStateProvider);
    final user = authState.user;

    return Scaffold(
      appBar: AppBar(
        title: const Text('USER PROFILE'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/dashboard'),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Center(
              child: Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: AppTheme.cardDark,
                  shape: BoxShape.circle,
                  border: Border.all(color: AppTheme.accentCyan, width: 2),
                ),
                child: const Icon(
                  Icons.person_outline,
                  size: 56,
                  color: AppTheme.accentCyan,
                ),
              ),
            ),
            const SizedBox(height: 16),
            Text(
              user?.username ?? 'Security User',
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            Text(
              user?.email ?? 'user@securityframework.io',
              style: const TextStyle(fontSize: 13, color: AppTheme.textMuted),
            ),
            const SizedBox(height: 24),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    _buildInfoRow('User UUID', user?.id ?? 'N/A'),
                    const Divider(color: Color(0xFF2E4057), height: 20),
                    _buildInfoRow(
                      'Assigned Roles',
                      user?.roles.join(', ') ?? 'ROLE_USER',
                    ),
                    const Divider(color: Color(0xFF2E4057), height: 20),
                    _buildInfoRow(
                      'Account Status',
                      user?.accountLocked == true ? 'LOCKED' : 'ACTIVE',
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                icon: const Icon(Icons.logout, size: 18),
                label: const Text('TERMINATE SESSION (LOGOUT)'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppTheme.failRed,
                  foregroundColor: Colors.white,
                ),
                onPressed: () async {
                  await ref.read(authStateProvider.notifier).logout();
                  if (context.mounted) {
                    context.go('/dashboard');
                  }
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          label,
          style: const TextStyle(fontSize: 13, color: AppTheme.textMuted),
        ),
        Text(
          value,
          style: const TextStyle(
            fontSize: 13,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
      ],
    );
  }
}
