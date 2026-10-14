import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../theme/app_theme.dart';
import '../../../auth/presentation/providers/auth_provider.dart';
import '../../../security/presentation/providers/security_provider.dart';
import '../providers/dashboard_provider.dart';
import '../widgets/advanced_banking_view.dart';
import '../widgets/advanced_healthcare_view.dart';
import '../widgets/vulnerability_lab_view.dart';

/// Central dashboard presenting real-time RASP diagnostics, cross-layer threat correlation,
/// risk-adaptive enforcement, and multi-domain reference applications (Banking & Healthcare).
class DashboardScreen extends ConsumerStatefulWidget {
  const DashboardScreen({super.key});

  @override
  ConsumerState<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends ConsumerState<DashboardScreen> {
  int _currentTab = 0;
  final TextEditingController _transferAmountController =
      TextEditingController(text: '500.00');
  final TextEditingController _recipientController =
      TextEditingController(text: 'alice@bank.vault');

  @override
  void dispose() {
    _transferAmountController.dispose();
    _recipientController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final dashboardView = ref.watch(dashboardViewProvider);
    final securityState = ref.watch(securityStateProvider);
    final authState = ref.watch(authStateProvider);
    final status = securityState.status;

    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: AppTheme.accentCyan.withOpacity(0.15),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: AppTheme.accentCyan.withOpacity(0.5)),
              ),
              child: const Icon(Icons.shield_outlined,
                  color: AppTheme.accentCyan, size: 20),
            ),
            const SizedBox(width: 10),
            const Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'APPSHIELDX',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w900,
                    letterSpacing: 1.5,
                  ),
                ),
                Text(
                  'Runtime Protection & API Security',
                  style: TextStyle(fontSize: 10, color: AppTheme.textMuted),
                ),
              ],
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Run Live RASP Diagnostic Scan',
            onPressed: securityState.isScanning
                ? null
                : () => ref
                    .read(securityStateProvider.notifier)
                    .scanRuntimeSecurity(),
          ),
          IconButton(
            icon: const Icon(Icons.settings_outlined),
            tooltip: 'Settings',
            onPressed: () => context.go('/settings'),
          ),
          IconButton(
            icon: Icon(
              authState.isAuthenticated ? Icons.person : Icons.login,
              color: authState.isAuthenticated
                  ? AppTheme.accentCyan
                  : Colors.white,
            ),
            tooltip: authState.isAuthenticated ? 'Profile' : 'Sign In',
            onPressed: () =>
                context.go(authState.isAuthenticated ? '/profile' : '/login'),
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          await ref.read(securityStateProvider.notifier).scanRuntimeSecurity();
        },
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Research Novelty: Server-Side Adaptive Zero-Trust Banner
              _buildAdaptivePolicyBanner(status),
              const SizedBox(height: 16),

              if (_currentTab == 0) ...[
                // TAB 0: RASP Security Engine & Attack Vectors
                _buildSecurityStatusCard(context, status, securityState.isScanning),
                const SizedBox(height: 16),
                _buildDemonstrationToolbar(context),
                const SizedBox(height: 16),
                _buildRecentEventsCard(context, securityState),
              ] else if (_currentTab == 1) ...[
                // TAB 1: Domain Client 1 - Secure Banking & Vault
                AdvancedBankingView(securityStatus: status),
              ] else if (_currentTab == 2) ...[
                // TAB 2: Advanced Clinical Healthcare EHR Portal
                AdvancedHealthcareView(securityStatus: status),
              ] else ...[
                // TAB 3: Vulnerability Lab - Vulnerable vs Protected App Showdown
                VulnerabilityLabView(securityStatus: status),
              ],
            ],
          ),
        ),
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentTab,
        onDestinationSelected: (index) => setState(() => _currentTab = index),
        backgroundColor: const Color(0xFF131926),
        indicatorColor: AppTheme.accentCyan.withOpacity(0.2),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.security, color: Colors.white70),
            selectedIcon: Icon(Icons.security, color: AppTheme.accentCyan),
            label: 'RASP Console',
          ),
          NavigationDestination(
            icon: Icon(Icons.account_balance, color: Colors.white70),
            selectedIcon:
                Icon(Icons.account_balance, color: AppTheme.accentCyan),
            label: 'Banking Vault',
          ),
          NavigationDestination(
            icon: Icon(Icons.local_hospital, color: Colors.white70),
            selectedIcon:
                Icon(Icons.local_hospital, color: Color(0xFF60A5FA)),
            label: 'Healthcare EHR',
          ),
          NavigationDestination(
            icon: Icon(Icons.compare_arrows, color: Colors.white70),
            selectedIcon:
                Icon(Icons.compare_arrows, color: AppTheme.warningAmber),
            label: 'Vulnerability Lab',
          ),
        ],
      ),
    );
  }

  Widget _buildDomainSwitcher() {
    return Container(
      decoration: BoxDecoration(
        color: const Color(0xFF1B2333),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFF2E4057)),
      ),
      padding: const EdgeInsets.all(4),
      child: Row(
        children: [
          _buildSwitcherTab(0, 'RASP Engine', Icons.security),
          _buildSwitcherTab(1, 'Banking Vault', Icons.account_balance_wallet),
          _buildSwitcherTab(2, 'Healthcare EHR', Icons.medical_services),
          _buildSwitcherTab(3, 'Vulnerability Lab', Icons.compare_arrows),
        ],
      ),
    );
  }

  Widget _buildSwitcherTab(int index, String title, IconData icon) {
    final isSelected = _currentTab == index;
    return Expanded(
      child: GestureDetector(
        onTap: () => setState(() => _currentTab = index),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 10),
          decoration: BoxDecoration(
            color: isSelected ? AppTheme.accentCyan.withOpacity(0.2) : Colors.transparent,
            borderRadius: BorderRadius.circular(8),
            border: isSelected
                ? Border.all(color: AppTheme.accentCyan)
                : Border.all(color: Colors.transparent),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                icon,
                size: 18,
                color: isSelected ? AppTheme.accentCyan : Colors.white60,
              ),
              const SizedBox(height: 4),
              Text(
                title,
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 10,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                  color: isSelected ? Colors.white : Colors.white60,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  /// Research Contribution: Dynamic Server-Side Adaptive Policy Banner
  Widget _buildAdaptivePolicyBanner(dynamic status) {
    final String risk = status?.riskLevel.toProtocolString() ?? 'LOW';
    int riskScore = 12;
    String band = 'ALLOW';
    String policy = 'Nominal Session • Full API Privileges Granted';
    Color bandColor = AppTheme.passGreen;

    if (risk == 'MEDIUM') {
      riskScore = 38;
      band = 'MONITOR';
      policy = 'Passive Telemetry Logging Active • Elevated Audit';
      bandColor = AppTheme.warningAmber;
    } else if (risk == 'HIGH') {
      riskScore = 65;
      band = 'STEP_UP_AUTHENTICATION';
      policy = 'Biometric / MFA Challenge Required for Sensitive Actions';
      bandColor = AppTheme.failRed;
    } else if (risk == 'CRITICAL') {
      riskScore = 88;
      band = 'RESTRICT_SENSITIVE_ACTIONS';
      policy = 'Zero-Trust Block: All Sensitive & Financial Endpoints Prohibited';
      bandColor = AppTheme.criticalPurple;
    }

    String badgeLabel = band;
    if (band == 'STEP_UP_AUTHENTICATION') {
      badgeLabel = 'STEP-UP AUTH';
    } else if (band == 'RESTRICT_SENSITIVE_ACTIONS') {
      badgeLabel = 'RESTRICTED';
    }

    return Card(
      color: const Color(0xFF172033),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
        side: BorderSide(color: bandColor.withOpacity(0.6), width: 1.5),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'CROSS-LAYER RISK SCORING ENGINE',
                        style: TextStyle(
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                          letterSpacing: 1.1,
                          color: AppTheme.textMuted,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Row(
                        children: [
                          Text(
                            '$riskScore',
                            style: TextStyle(
                              fontSize: 26,
                              fontWeight: FontWeight.w900,
                              color: bandColor,
                            ),
                          ),
                          const Text(
                            ' / 100',
                            style: TextStyle(fontSize: 13, color: AppTheme.textMuted),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 8),
                Flexible(
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                    decoration: BoxDecoration(
                      color: bandColor.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: bandColor),
                    ),
                    child: Text(
                      badgeLabel,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: TextStyle(
                        color: bandColor,
                        fontSize: 10,
                        fontWeight: FontWeight.w900,
                        letterSpacing: 0.5,
                      ),
                    ),
                  ),
                ),
              ],
            ),
            const Divider(color: Color(0xFF2E4057), height: 20),
            Row(
              children: [
                Icon(
                  band == 'ALLOW' ? Icons.verified_user : Icons.gpp_bad,
                  size: 16,
                  color: bandColor,
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    policy,
                    style: TextStyle(fontSize: 11, color: Colors.white70),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  /// Reference App 1: Banking & Financial Vault
  Widget _buildBankingClientView(dynamic status) {
    final bool isBlocked = status?.riskLevel.toProtocolString() == 'CRITICAL';

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Row(
                  children: [
                    Icon(Icons.account_balance, color: AppTheme.accentCyan, size: 20),
                    SizedBox(width: 8),
                    Text(
                      'SECURE BANKING CLIENT',
                      style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: Colors.white10,
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: const Text('Domain App 1',
                      style: TextStyle(fontSize: 10, color: AppTheme.accentCyan)),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [Color(0xFF1E3A8A), Color(0xFF0F172A)],
                ),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('PRIMARY VAULT BALANCE',
                      style: TextStyle(fontSize: 11, color: Colors.white70)),
                  const SizedBox(height: 6),
                  const Text('\$48,250.00 USD',
                      style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.white)),
                  const SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('Account: •••• •••• •••• 8291',
                          style: TextStyle(fontSize: 11, color: Colors.white60)),
                      Text(isBlocked ? 'ACCESS RESTRICTED' : 'VERIFIED TIER',
                          style: TextStyle(
                              fontSize: 10,
                              fontWeight: FontWeight.bold,
                              color: isBlocked ? AppTheme.failRed : AppTheme.passGreen)),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),
            const Text('INITIATE WIRE TRANSFER',
                style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            TextField(
              controller: _recipientController,
              decoration: const InputDecoration(
                labelText: 'Recipient IBAN / Email',
                prefixIcon: Icon(Icons.person_outline, size: 18),
                isDense: true,
              ),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _transferAmountController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Amount (\$ USD)',
                prefixIcon: Icon(Icons.attach_money, size: 18),
                isDense: true,
              ),
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                icon: Icon(isBlocked ? Icons.block : Icons.send, size: 18),
                label: Text(
                  isBlocked
                      ? 'TRANSFER RESTRICTED BY SERVER POLICY'
                      : 'EXECUTE SECURE TRANSFER',
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: isBlocked ? AppTheme.failRed : AppTheme.accentCyan,
                  padding: const EdgeInsets.symmetric(vertical: 14),
                ),
                onPressed: () => _executeBankingTransaction(context, isBlocked),
              ),
            ),
            const SizedBox(height: 12),
            const Text(
              'Demonstration Note: When RASP probes detect runtime hooks or root privileges, the Server Zero-Trust Filter immediately returns HTTP 403, blocking transactions even if client code is modified.',
              style: TextStyle(fontSize: 10, color: AppTheme.textMuted, fontStyle: FontStyle.italic),
            ),
          ],
        ),
      ),
    );
  }

  void _executeBankingTransaction(BuildContext context, bool isBlocked) {
    if (isBlocked) {
      showDialog(
        context: context,
        builder: (ctx) => AlertDialog(
          backgroundColor: const Color(0xFF1E283D),
          title: const Row(
            children: [
              Icon(Icons.security, color: AppTheme.failRed),
              SizedBox(width: 8),
              Text('ZERO-TRUST RESTRICTION'),
            ],
          ),
          content: const Text(
            'HTTP 403 FORBIDDEN\n\nEnforcement Band: RESTRICT_SENSITIVE_ACTIONS\nServer Risk Score: 88 / 100\n\nThe transaction was blocked by the Spring Cloud Gateway and ZeroTrustSecurityFilter because active mobile runtime tampering (Frida / Root / Debugger) was detected on this device.',
            style: TextStyle(fontSize: 13, height: 1.4),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(ctx),
              child: const Text('DISMISS', style: TextStyle(color: AppTheme.accentCyan)),
            ),
          ],
        ),
      );
    } else {
      showDialog(
        context: context,
        builder: (ctx) => AlertDialog(
          backgroundColor: const Color(0xFF1E283D),
          title: const Row(
            children: [
              Icon(Icons.check_circle, color: AppTheme.passGreen),
              SizedBox(width: 8),
              Text('TRANSFER APPROVED'),
            ],
          ),
          content: Text(
            'Transfer of \$${_transferAmountController.text} to ${_recipientController.text} processed successfully.\n\nEnforcement Band: ALLOW\nDevice Fingerprint Verified.',
            style: const TextStyle(fontSize: 13, height: 1.4),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(ctx),
              child: const Text('OK', style: TextStyle(color: AppTheme.passGreen)),
            ),
          ],
        ),
      );
    }
  }

  /// Reference App 2: Healthcare Patient Portal (Cross-Domain Reusability)
  Widget _buildHealthcareClientView(dynamic status) {
    final bool isBlocked = status?.riskLevel.toProtocolString() == 'CRITICAL';

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Row(
                  children: [
                    Icon(Icons.medical_services, color: AppTheme.accentCyan, size: 20),
                    SizedBox(width: 8),
                    Text(
                      'HEALTHCARE CLINICAL PORTAL',
                      style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: Colors.white10,
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: const Text('Domain App 2',
                      style: TextStyle(fontSize: 10, color: Color(0xFF64B5F6))),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: const Color(0xFF111827),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: const Color(0xFF1F2937)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text('PATIENT: John Doe (ID: #EHR-94021)',
                          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                      Text('AGE: 42 • O+', style: TextStyle(fontSize: 11, color: AppTheme.textMuted)),
                    ],
                  ),
                  const SizedBox(height: 8),
                  const Text('Diagnosis: Hypertension Stage 1 / Elevated Cardiology Markers',
                      style: TextStyle(fontSize: 11, color: Colors.white70)),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                        decoration: BoxDecoration(
                          color: AppTheme.warningAmber.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: const Text('CONFIDENTIAL PHI',
                            style: TextStyle(color: AppTheme.warningAmber, fontSize: 9, fontWeight: FontWeight.bold)),
                      ),
                      const SizedBox(width: 8),
                      const Text('HIPAA / GDPR Protection Enforced',
                          style: TextStyle(fontSize: 10, color: AppTheme.textMuted)),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                icon: Icon(isBlocked ? Icons.lock : Icons.assignment_turned_in, size: 18),
                label: Text(
                  isBlocked
                      ? 'EHR ACCESS RESTRICTED BY RASP POLICY'
                      : 'APPROVE CLINICAL PRESCRIPTION',
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: isBlocked ? AppTheme.failRed : const Color(0xFF2563EB),
                  padding: const EdgeInsets.symmetric(vertical: 14),
                ),
                onPressed: () => _executeBankingTransaction(context, isBlocked),
              ),
            ),
            const SizedBox(height: 10),
            const Text(
              'Research Validation: Demonstrates AppShieldX SDK integrating into a second distinct domain (EHR Healthcare) using identical telemetry, zero-trust enforcement, and correlation models.',
              style: TextStyle(fontSize: 10, color: AppTheme.textMuted, fontStyle: FontStyle.italic),
            ),
          ],
        ),
      ),
    );
  }

  /// Core RASP Diagnostic Status Card
  Widget _buildSecurityStatusCard(
    BuildContext context,
    dynamic status,
    bool isScanning,
  ) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Row(
                  children: [
                    Icon(Icons.verified_outlined, color: AppTheme.accentCyan, size: 20),
                    SizedBox(width: 8),
                    Text(
                      'Runtime Protection Probes',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                  ],
                ),
                if (isScanning)
                  const SizedBox(
                    width: 16,
                    height: 16,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  ),
              ],
            ),
            const SizedBox(height: 16),
            _buildStatusRow(
              'Root & Privilege Escalation',
              !(status?.rootDetected ?? false),
            ),
            _buildStatusRow(
              'Jailbreak & Sandbox Integrity',
              !(status?.jailbreakDetected ?? false),
            ),
            _buildStatusRow(
              'Active Debugger / Tracer Attached',
              !(status?.debuggerDetected ?? false),
            ),
            _buildStatusRow(
              'Frida / Dynamic Hooking Framework',
              !(status?.fridaDetected ?? false),
            ),
            _buildStatusRow(
              'Application Binary Integrity (Signature)',
              status?.integrityValid ?? true,
            ),
            _buildStatusRow(
              'TLS Certificate Pinning',
              status?.sslPinningEnabled ?? true,
            ),
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                icon: const Icon(Icons.analytics_outlined, size: 18),
                label: const Text('Detailed Diagnostics & Telemetry Log'),
                style: OutlinedButton.styleFrom(
                  side: const BorderSide(color: Color(0xFF2E4057)),
                ),
                onPressed: () => context.go('/security-status'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatusRow(String label, bool isPass) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontSize: 13, color: Colors.white70)),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
            decoration: BoxDecoration(
              color: isPass
                  ? AppTheme.passGreen.withOpacity(0.15)
                  : AppTheme.failRed.withOpacity(0.15),
              borderRadius: BorderRadius.circular(6),
              border: Border.all(
                color: isPass ? AppTheme.passGreen : AppTheme.failRed,
                width: 1,
              ),
            ),
            child: Text(
              isPass ? 'PASS' : 'FAIL',
              style: TextStyle(
                fontSize: 11,
                fontWeight: FontWeight.w900,
                color: isPass ? AppTheme.passGreen : AppTheme.failRed,
                letterSpacing: 0.8,
              ),
            ),
          ),
        ],
      ),
    );
  }

  /// Examiner Demonstration Toolbar
  Widget _buildDemonstrationToolbar(BuildContext context) {
    return Card(
      color: const Color(0xFF1E283D),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              children: [
                Icon(Icons.science_outlined, color: AppTheme.warningAmber, size: 18),
                SizedBox(width: 8),
                Text(
                  'Demonstration: Trigger RASP Attack Vector',
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 6),
            const Text(
              'Simulate how the framework responds, calculates risk, and streams telemetry to the SOC dashboard.',
              style: TextStyle(fontSize: 11, color: AppTheme.textMuted),
            ),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                _buildSimulationChip(
                  'Simulate Frida',
                  'FRIDA_DETECTED',
                  AppTheme.criticalPurple,
                ),
                _buildSimulationChip(
                  'Simulate Root',
                  'ROOT_DETECTED',
                  AppTheme.failRed,
                ),
                _buildSimulationChip(
                  'Simulate Debugger',
                  'DEBUGGER_DETECTED',
                  AppTheme.warningAmber,
                ),
                _buildSimulationChip(
                  'Simulate Tamper',
                  'TAMPERING_DETECTED',
                  AppTheme.failRed,
                ),
              ],
            ),
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: TextButton.icon(
                icon: const Icon(Icons.restart_alt, size: 16),
                label: const Text('Reset Security State to Nominal'),
                style: TextButton.styleFrom(
                  foregroundColor: AppTheme.accentCyan,
                ),
                onPressed: () async {
                  await ref
                      .read(securityStateProvider.notifier)
                      .scanRuntimeSecurity();
                  if (context.mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text('Security status reset to NOMINAL.'),
                        backgroundColor: AppTheme.passGreen,
                      ),
                    );
                  }
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSimulationChip(
    String label,
    String eventType,
    Color color,
  ) {
    return ActionChip(
      backgroundColor: color.withOpacity(0.12),
      side: BorderSide(color: color.withOpacity(0.6)),
      label: Text(
        label,
        style: TextStyle(color: color, fontSize: 11, fontWeight: FontWeight.bold),
      ),
      onPressed: () {
        ref.read(securityStateProvider.notifier).simulateThreat(eventType);
      },
    );
  }

  Widget _buildRecentEventsCard(
    BuildContext context,
    SecurityState state,
  ) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  'Recent Security Events',
                  style: TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                if (state.offlineQueueCount > 0)
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                    decoration: BoxDecoration(
                      color: AppTheme.warningAmber.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: AppTheme.warningAmber),
                    ),
                    child: Text(
                      '${state.offlineQueueCount} Offline Queued',
                      style: const TextStyle(
                        color: AppTheme.warningAmber,
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 12),
            if (state.recentEvents.isEmpty)
              const Padding(
                padding: EdgeInsets.symmetric(vertical: 16),
                child: Center(
                  child: Text(
                    'No security incidents recorded. System nominal.',
                    style: TextStyle(color: AppTheme.textMuted, fontSize: 12),
                  ),
                ),
              )
            else
              ListView.separated(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: state.recentEvents.take(5).length,
                separatorBuilder: (_, __) =>
                    const Divider(color: Color(0xFF2E4057), height: 12),
                itemBuilder: (context, index) {
                  final event = state.recentEvents[index];
                  return Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            event.eventType,
                            style: const TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),
                          Text(
                            event.description,
                            style: const TextStyle(
                              fontSize: 10,
                              color: AppTheme.textMuted,
                            ),
                          ),
                        ],
                      ),
                      Text(
                        event.severity,
                        style: TextStyle(
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                          color: event.severity == 'CRITICAL'
                              ? AppTheme.criticalPurple
                              : event.severity == 'HIGH'
                                  ? AppTheme.failRed
                                  : AppTheme.warningAmber,
                        ),
                      ),
                    ],
                  );
                },
              ),
            const SizedBox(height: 10),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                TextButton(
                  onPressed: () => context.go('/security-events'),
                  child: const Text('View All Events',
                      style: TextStyle(color: AppTheme.accentCyan, fontSize: 12)),
                ),
                if (state.offlineQueueCount > 0)
                  ElevatedButton.icon(
                    icon: const Icon(Icons.cloud_upload_outlined, size: 14),
                    label: const Text('Flush Queue', style: TextStyle(fontSize: 11)),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    ),
                    onPressed: () async {
                      final count = await ref
                          .read(securityStateProvider.notifier)
                          .flushQueue();
                      if (context.mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text('Transmitted $count security events.'),
                            backgroundColor: AppTheme.passGreen,
                          ),
                        );
                      }
                    },
                  ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
