import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';

/// Advanced Cyber-Grade Banking & Financial Vault View
/// Features multi-asset portfolio, dynamic zero-trust transaction evaluation,
/// hardware-backed cryptographic signing, and real-time policy blocking.
class AdvancedBankingView extends StatefulWidget {
  final dynamic securityStatus;

  const AdvancedBankingView({super.key, required this.securityStatus});

  @override
  State<AdvancedBankingView> createState() => _AdvancedBankingViewState();
}

class _AdvancedBankingViewState extends State<AdvancedBankingView> {
  int _selectedAccountIndex = 0;
  final TextEditingController _recipientController =
      TextEditingController(text: 'alice@bank.vault');
  final TextEditingController _amountController =
      TextEditingController(text: '5000.00');

  String _selectedJurisdiction = 'Domestic (US-ACH)';
  bool _isEvaluating = false;
  bool _simulateAdbDebugging = false;

  final List<Map<String, dynamic>> _accounts = [
    {
      'title': 'GLOBAL CORPORATE TREASURY',
      'currency': 'USD',
      'balance': '\$148,250.00',
      'accountNumber': '•••• •••• •••• 8291',
      'type': 'Fiat Liquidity Vault',
      'gradient': [const Color(0xFF1E3A8A), const Color(0xFF0F172A)],
      'chipColor': AppTheme.accentCyan,
    },
    {
      'title': 'COLD MULTI-SIG CRYPTO VAULT',
      'currency': 'BTC',
      'balance': '3.85 BTC (\$245,600.00)',
      'accountNumber': 'bc1q9a4f78de2...99a0',
      'type': 'Hardware Enclave SegWit',
      'gradient': [const Color(0xFFD97706), const Color(0xFF451A03)],
      'chipColor': const Color(0xFFFBBF24),
    },
    {
      'title': 'SOVEREIGN BULLION RESERVE',
      'currency': 'XAU',
      'balance': '500.00g (\$38,200.00)',
      'accountNumber': 'VAULT-ZURICH-CH-004',
      'type': 'Physical Custody Vault',
      'gradient': [const Color(0xFF065F46), const Color(0xFF064E3B)],
      'chipColor': AppTheme.passGreen,
    },
  ];

  final List<Map<String, dynamic>> _transactions = [
    {
      'title': 'Apex Supply Chain Payment',
      'dest': 'Domestic ACH • US-FEDWIRE',
      'amount': '-\$12,450.00',
      'time': '10 mins ago',
      'riskScore': 8,
      'riskBand': 'LOW',
      'color': AppTheme.passGreen,
      'icon': Icons.arrow_upward,
    },
    {
      'title': 'Offshore Wire Transfer Attempt',
      'dest': 'Cayman Islands Shell Entity',
      'amount': '-\$75,000.00',
      'time': '1 hour ago',
      'riskScore': 86,
      'riskBand': 'CRITICAL (BLOCKED)',
      'color': AppTheme.failRed,
      'icon': Icons.block,
    },
    {
      'title': 'Zurich Cash Reserve Dispense',
      'dest': 'ATM Vault Biometric POS',
      'amount': '-\$2,000.00',
      'time': '3 hours ago',
      'riskScore': 42,
      'riskBand': 'MEDIUM (STEP-UP MFA)',
      'color': AppTheme.warningAmber,
      'icon': Icons.verified_user,
    },
  ];

  @override
  void dispose() {
    _recipientController.dispose();
    _amountController.dispose();
    super.dispose();
  }

  int _calculatePreFlightRiskScore() {
    final status = widget.securityStatus;
    int baseScore = 10;

    final bool isDebuggerActive = _simulateAdbDebugging;

    // Check device RASP status
    if (status?.rootDetected ?? false) baseScore += 50;
    if (status?.jailbreakDetected ?? false) baseScore += 50;
    if (status?.fridaDetected ?? false) baseScore += 60;
    if (isDebuggerActive) baseScore += 75;
    if (!(status?.integrityValid ?? true)) baseScore += 45;

    // Jurisdiction weighting
    if (_selectedJurisdiction == 'Offshore / High-Risk Non-FATF') {
      baseScore += 30;
    }

    // Amount weighting
    final double amount = double.tryParse(_amountController.text) ?? 0.0;
    if (amount > 10000.0) {
      baseScore += 15;
    }
    if (amount > 50000.0) {
      baseScore += 25;
    }

    return baseScore.clamp(0, 100);
  }

  void _executeTransfer() {
    final bool isDebugger = _simulateAdbDebugging;
    final score = _calculatePreFlightRiskScore();
    final bool isBlocked = isDebugger ||
        score >= 60 ||
        (widget.securityStatus?.riskLevel.toProtocolString() == 'CRITICAL');

    setState(() => _isEvaluating = true);

    Future.delayed(const Duration(milliseconds: 700), () {
      if (!mounted) return;
      setState(() => _isEvaluating = false);

      if (isBlocked) {
        showDialog(
          context: context,
          builder: (ctx) => AlertDialog(
            backgroundColor: const Color(0xFF161F30),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
              side: const BorderSide(color: AppTheme.failRed, width: 2),
            ),
            title: Row(
              children: [
                Icon(isDebugger ? Icons.usb_off : Icons.shield,
                    color: AppTheme.failRed, size: 28),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    isDebugger
                        ? 'PAYMENT STRICTLY BLOCKED (NON-BYPASSABLE)'
                        : 'ZERO-TRUST INTERCEPT',
                    style: const TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.failRed,
                    ),
                  ),
                ),
              ],
            ),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: AppTheme.failRed.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('GATEWAY RESPONSE:',
                          style: TextStyle(
                              fontSize: 10, fontWeight: FontWeight.bold)),
                      Text('HTTP 403 FORBIDDEN',
                          style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.bold,
                              color: AppTheme.failRed)),
                    ],
                  ),
                ),
                const SizedBox(height: 12),
                if (isDebugger) ...[
                  const Text(
                    'VIOLATION: USB DEBUGGING / ADB ACTIVE\n\n'
                    'COMMERCIAL BANK MODEL (HDFC Flaw):\n'
                    'Legacy apps show a warning banner but provide a [SKIP] button, allowing payments to succeed despite active ADB debugging.\n\n'
                    'APPSHIELDX ZERO-TRUST MODEL:\n'
                    'AppShieldX enforces non-bypassable policy quarantine. NO SKIP OPTION EXISTS. Financial endpoints are 100% blocked until USB Debugging is turned OFF in Android Developer Options.',
                    style: TextStyle(fontSize: 11, height: 1.45),
                  ),
                ] else ...[
                  Text(
                    'Composite Risk Score: $score / 100 [CRITICAL]\nEnforcement Band: RESTRICT_SENSITIVE_ACTIONS\n\nThe transaction of \$${_amountController.text} to ${_recipientController.text} was intercepted by the Spring Cloud Gateway ZeroTrustSecurityFilter.',
                    style: const TextStyle(fontSize: 12, height: 1.4),
                  ),
                  const SizedBox(height: 12),
                  const Text(
                    'Triggers Detected:\n• High-Risk Jurisdiction or Amount Threshold Exceeded\n• RASP Device Integrity Violation / Kernel Tampering Active\n• Device Fingerprint Quarantined in AWS CloudWatch',
                    style: TextStyle(fontSize: 11, color: AppTheme.textMuted),
                  ),
                ],
              ],
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(ctx),
                child: Text(
                    isDebugger
                        ? 'I UNDERSTAND (CANNOT BYPASS)'
                        : 'DISMISS',
                    style: const TextStyle(color: AppTheme.accentCyan, fontWeight: FontWeight.bold)),
              ),
            ],
          ),
        );
      } else {
        showDialog(
          context: context,
          builder: (ctx) => AlertDialog(
            backgroundColor: const Color(0xFF161F30),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
              side: const BorderSide(color: AppTheme.passGreen, width: 2),
            ),
            title: const Row(
              children: [
                Icon(Icons.verified, color: AppTheme.passGreen, size: 28),
                SizedBox(width: 10),
                Text(
                  'TRANSACTION SIGNED',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: AppTheme.passGreen,
                  ),
                ),
              ],
            ),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Wire of \$${_amountController.text} to ${_recipientController.text} cryptographically committed to Spring Cloud Gateway.',
                  style: const TextStyle(fontSize: 13, height: 1.4),
                ),
                const SizedBox(height: 12),
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: const Color(0xFF0D1117),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: const Color(0xFF283548)),
                  ),
                  child: const Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('ENCLAVE SIGNATURE:',
                          style: TextStyle(
                              fontSize: 9,
                              fontWeight: FontWeight.bold,
                              color: AppTheme.accentCyan)),
                      SizedBox(height: 4),
                      Text('ECDSA_SECP256R1: 0x9f4a...812d',
                          style: TextStyle(
                              fontSize: 10,
                              fontFamily: 'monospace',
                              color: Colors.white70)),
                      SizedBox(height: 6),
                      Text('TLS 1.3 CIPHER:',
                          style: TextStyle(
                              fontSize: 9,
                              fontWeight: FontWeight.bold,
                              color: AppTheme.accentCyan)),
                      SizedBox(height: 4),
                      Text('TLS_AES_256_GCM_SHA384 (Certificate Pinned)',
                          style: TextStyle(
                              fontSize: 10,
                              fontFamily: 'monospace',
                              color: Colors.white70)),
                    ],
                  ),
                ),
              ],
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(ctx),
                child: const Text('OK',
                    style: TextStyle(color: AppTheme.passGreen)),
              ),
            ],
          ),
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final curAccount = _accounts[_selectedAccountIndex];
    final bool isUsbDebuggerActive = _simulateAdbDebugging;
    final score = _calculatePreFlightRiskScore();
    final bool isHighRisk = score >= 60 || isUsbDebuggerActive;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // Account Portfolio Carousel
        SizedBox(
          height: 190,
          child: PageView.builder(
            itemCount: _accounts.length,
            onPageChanged: (i) => setState(() => _selectedAccountIndex = i),
            itemBuilder: (context, i) {
              final acc = _accounts[i];
              return Container(
                margin: const EdgeInsets.symmetric(horizontal: 4),
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: acc['gradient'] as List<Color>,
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(18),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.4),
                      blurRadius: 10,
                      offset: const Offset(0, 4),
                    ),
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          acc['title'] as String,
                          style: const TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.bold,
                            letterSpacing: 1.1,
                            color: Colors.white70,
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 8, vertical: 3),
                          decoration: BoxDecoration(
                            color: Colors.white.withOpacity(0.15),
                            borderRadius: BorderRadius.circular(6),
                          ),
                          child: Text(
                            acc['type'] as String,
                            style: TextStyle(
                              fontSize: 9,
                              fontWeight: FontWeight.bold,
                              color: acc['chipColor'] as Color,
                            ),
                          ),
                        ),
                      ],
                    ),
                    Text(
                      acc['balance'] as String,
                      style: const TextStyle(
                        fontSize: 26,
                        fontWeight: FontWeight.w900,
                        color: Colors.white,
                      ),
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          acc['accountNumber'] as String,
                          style: const TextStyle(
                            fontSize: 12,
                            fontFamily: 'monospace',
                            color: Colors.white60,
                          ),
                        ),
                        const Row(
                          children: [
                            Icon(Icons.lock, size: 12, color: AppTheme.passGreen),
                            SizedBox(width: 4),
                            Text('KEYSTORE ATTESTED',
                                style: TextStyle(
                                    fontSize: 9,
                                    fontWeight: FontWeight.bold,
                                    color: AppTheme.passGreen)),
                          ],
                        ),
                      ],
                    ),
                  ],
                ),
              );
            },
          ),
        ),
        const SizedBox(height: 8),

        // Indicator dots
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: List.generate(
            _accounts.length,
            (i) => Container(
              margin: const EdgeInsets.symmetric(horizontal: 3),
              width: _selectedAccountIndex == i ? 16 : 6,
              height: 6,
              decoration: BoxDecoration(
                color: _selectedAccountIndex == i
                    ? AppTheme.accentCyan
                    : Colors.white24,
                borderRadius: BorderRadius.circular(3),
              ),
            ),
          ),
        ),
        const SizedBox(height: 16),

        // Wire Transfer Panel
        Card(
          color: const Color(0xFF161B26),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
            side: BorderSide(
              color: isUsbDebuggerActive ? AppTheme.failRed : const Color(0xFF283548),
              width: isUsbDebuggerActive ? 1.5 : 1.0,
            ),
          ),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    const Icon(Icons.swap_horiz,
                        color: AppTheme.accentCyan, size: 20),
                    const SizedBox(width: 8),
                    const Expanded(
                      child: Text(
                        'ZERO-TRUST WIRE TRANSFER CONSOLE',
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          letterSpacing: 0.5,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    if (isUsbDebuggerActive) ...[
                      const SizedBox(width: 6),
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 6, vertical: 2),
                        decoration: BoxDecoration(
                          color: AppTheme.failRed.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(4),
                          border: Border.all(color: AppTheme.failRed, width: 0.8),
                        ),
                        child: const Text('ADB LOCKED',
                            style: TextStyle(
                                fontSize: 9,
                                fontWeight: FontWeight.bold,
                                color: AppTheme.failRed)),
                      ),
                    ],
                  ],
                ),
                const SizedBox(height: 12),

                // ADB Simulation Control for Evaluators
                Container(
                  padding: const EdgeInsets.symmetric(
                      horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: _simulateAdbDebugging
                        ? AppTheme.failRed.withOpacity(0.12)
                        : const Color(0xFF0F1523),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(
                      color: _simulateAdbDebugging
                          ? AppTheme.failRed
                          : const Color(0xFF283548),
                    ),
                  ),
                  child: Row(
                    children: [
                      Icon(
                        Icons.adb,
                        size: 16,
                        color: _simulateAdbDebugging
                            ? AppTheme.failRed
                            : AppTheme.textMuted,
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          'Simulate USB Debugger Active:',
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.bold,
                            color: _simulateAdbDebugging
                                ? AppTheme.failRed
                                : AppTheme.textMuted,
                          ),
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                      Switch(
                        value: _simulateAdbDebugging,
                        activeColor: AppTheme.failRed,
                        onChanged: (val) {
                          setState(() => _simulateAdbDebugging = val);
                        },
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 14),

                // Recipient
                TextField(
                  controller: _recipientController,
                  decoration: const InputDecoration(
                    labelText: 'Recipient IBAN / Vault Identifier',
                    prefixIcon: Icon(Icons.account_circle_outlined, size: 18),
                    isDense: true,
                  ),
                ),
                const SizedBox(height: 10),

                // Quick Recipient Chips
                Wrap(
                  spacing: 6,
                  children: [
                    ActionChip(
                      label: const Text('Alice (Whitelisted)',
                          style: TextStyle(fontSize: 10)),
                      onPressed: () => setState(() =>
                          _recipientController.text = 'alice@bank.vault'),
                    ),
                    ActionChip(
                      label: const Text('Apex Corp (Domestic)',
                          style: TextStyle(fontSize: 10)),
                      onPressed: () => setState(() =>
                          _recipientController.text = 'treasury@apexlogistics.com'),
                    ),
                    ActionChip(
                      label: const Text('Cayman Entity (Offshore)',
                          style: TextStyle(fontSize: 10)),
                      onPressed: () => setState(() =>
                          _recipientController.text = 'holding@caiman-dark.vg'),
                    ),
                  ],
                ),
                const SizedBox(height: 12),

                // Amount
                TextField(
                  controller: _amountController,
                  keyboardType: TextInputType.number,
                  onChanged: (_) => setState(() {}),
                  decoration: const InputDecoration(
                    labelText: 'Transfer Amount (\$ USD)',
                    prefixIcon: Icon(Icons.attach_money, size: 18),
                    isDense: true,
                  ),
                ),
                const SizedBox(height: 10),

                // Quick Amount Chips
                Wrap(
                  spacing: 6,
                  children: [
                    ActionChip(
                      label: const Text('\$500', style: TextStyle(fontSize: 10)),
                      onPressed: () => setState(
                          () => _amountController.text = '500.00'),
                    ),
                    ActionChip(
                      label: const Text('\$5,000', style: TextStyle(fontSize: 10)),
                      onPressed: () => setState(
                          () => _amountController.text = '5000.00'),
                    ),
                    ActionChip(
                      label: const Text('\$25,000', style: TextStyle(fontSize: 10)),
                      onPressed: () => setState(
                          () => _amountController.text = '25000.00'),
                    ),
                    ActionChip(
                      label: const Text('\$100,000 (High Risk)',
                          style: TextStyle(fontSize: 10)),
                      onPressed: () => setState(
                          () => _amountController.text = '100000.00'),
                    ),
                  ],
                ),
                const SizedBox(height: 14),

                // Jurisdiction Dropdown
                DropdownButtonFormField<String>(
                  value: _selectedJurisdiction,
                  isExpanded: true,
                  decoration: const InputDecoration(
                    labelText: 'Destination Jurisdiction',
                    prefixIcon: Icon(Icons.public, size: 18),
                    isDense: true,
                    contentPadding:
                        EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                  ),
                  items: const [
                    DropdownMenuItem(
                      value: 'Domestic (US-ACH)',
                      child: Text('Domestic (US-ACH • Low Risk)',
                          overflow: TextOverflow.ellipsis),
                    ),
                    DropdownMenuItem(
                      value: 'EU SEPA Cross-Border',
                      child: Text('EU SEPA Cross-Border (Medium Risk)',
                          overflow: TextOverflow.ellipsis),
                    ),
                    DropdownMenuItem(
                      value: 'Offshore / High-Risk Non-FATF',
                      child: Text('Offshore / High-Risk Non-FATF',
                          overflow: TextOverflow.ellipsis),
                    ),
                  ],
                  onChanged: (val) {
                    if (val != null) setState(() => _selectedJurisdiction = val);
                  },
                ),
                const SizedBox(height: 16),

                // Real-Time Pre-Flight Assessment Bar
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: const Color(0xFF0F1523),
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(
                      color: isHighRisk
                          ? AppTheme.failRed.withOpacity(0.5)
                          : AppTheme.passGreen.withOpacity(0.5),
                    ),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text('PRE-FLIGHT ZERO-TRUST SCORE',
                              style: TextStyle(
                                  fontSize: 9,
                                  fontWeight: FontWeight.bold,
                                  color: AppTheme.textMuted)),
                          const SizedBox(height: 2),
                          Text(
                            '$score / 100',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w900,
                              color: isHighRisk
                                  ? AppTheme.failRed
                                  : AppTheme.passGreen,
                            ),
                          ),
                        ],
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: (isHighRisk
                                  ? AppTheme.failRed
                                  : AppTheme.passGreen)
                              .withOpacity(0.2),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          isHighRisk ? 'RESTRICTED' : 'CLEAR TO DISPATCH',
                          style: TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.bold,
                            color: isHighRisk
                                ? AppTheme.failRed
                                : AppTheme.passGreen,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 16),

                // Submit Button
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    icon: _isEvaluating
                        ? const SizedBox(
                            width: 18,
                            height: 18,
                            child: CircularProgressIndicator(
                              strokeWidth: 2,
                              color: Colors.white,
                            ),
                          )
                        : Icon(isHighRisk ? Icons.block : Icons.lock_open,
                            size: 18),
                    label: Text(
                      _isEvaluating
                          ? 'EVALUATING GATEWAY POLICIES...'
                          : (isUsbDebuggerActive
                              ? '⛔ PAYMENT HARD-BLOCKED (USB DEBUGGER ACTIVE)'
                              : (isHighRisk
                                  ? 'EXECUTE (TRIGGER ZERO-TRUST 403 BLOCK)'
                                  : 'COMMIT CRYPTOGRAPHIC TRANSFER')),
                      overflow: TextOverflow.ellipsis,
                    ),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: isHighRisk
                          ? AppTheme.failRed
                          : AppTheme.accentCyan,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10),
                      ),
                    ),
                    onPressed: _isEvaluating ? null : _executeTransfer,
                  ),
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),

        // Live Transaction Stream
        const Text(
          'AUDIT TRAIL & TRANSACTION STREAM:',
          style: TextStyle(
            fontSize: 11,
            fontWeight: FontWeight.bold,
            letterSpacing: 1,
            color: AppTheme.textMuted,
          ),
        ),
        const SizedBox(height: 8),
        ..._transactions.map((t) => Card(
              color: const Color(0xFF131926),
              margin: const EdgeInsets.only(bottom: 8),
              child: ListTile(
                leading: CircleAvatar(
                  backgroundColor: (t['color'] as Color).withOpacity(0.2),
                  child: Icon(t['icon'] as IconData,
                      color: t['color'] as Color, size: 18),
                ),
                title: Text(t['title'] as String,
                    style: const TextStyle(
                        fontSize: 13, fontWeight: FontWeight.bold)),
                subtitle: Text('${t['dest']} • ${t['time']}',
                    style:
                        const TextStyle(fontSize: 11, color: AppTheme.textMuted)),
                trailing: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Text(t['amount'] as String,
                        style: const TextStyle(
                            fontSize: 13, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 2),
                    Text(
                      t['riskBand'] as String,
                      style: TextStyle(
                        fontSize: 9,
                        fontWeight: FontWeight.bold,
                        color: t['color'] as Color,
                      ),
                    ),
                  ],
                ),
              ),
            )),
      ],
    );
  }
}
