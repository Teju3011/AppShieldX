import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../auth/presentation/providers/auth_provider.dart';
import '../../../security/presentation/providers/security_provider.dart';

/// Aggregated view state representing all high-level operational indicators.
class DashboardViewState {
  final String authStatusText;
  final String apiConnectionStatus;
  final bool isSecure;

  const DashboardViewState({
    required this.authStatusText,
    required this.apiConnectionStatus,
    required this.isSecure,
  });
}

final dashboardViewProvider = Provider<DashboardViewState>((ref) {
  final authState = ref.watch(authStateProvider);
  final securityState = ref.watch(securityStateProvider);

  final authText = authState.isAuthenticated
      ? 'AUTHENTICATED (${authState.user?.username ?? 'User'})'
      : 'ANONYMOUS / GUEST';

  final bool compromised = securityState.status?.isCompromised ?? false;

  return DashboardViewState(
    authStatusText: authText,
    apiConnectionStatus: 'CONNECTED (TLS 1.3)',
    isSecure: !compromised,
  );
});
