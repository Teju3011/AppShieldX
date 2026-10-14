import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../theme/app_theme.dart';
import '../providers/security_provider.dart';

/// Detailed diagnostic screen analyzing individual RASP probes and risk scoring calculations.
class SecurityStatusScreen extends ConsumerWidget {
  const SecurityStatusScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final securityState = ref.watch(securityStateProvider);
    final status = securityState.status;

    return Scaffold(
      appBar: AppBar(
        title: const Text('RASP DIAGNOSTICS'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/dashboard'),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Device Telemetry Header
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'DEVICE FINGERPRINT & HOST CONTEXT',
                      style: TextStyle(
                        fontSize: 11,
                        color: AppTheme.textMuted,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Hardware ID: ${status?.deviceId ?? "Resolving..."}',
                      style: const TextStyle(
                        fontSize: 12,
                        fontFamily: 'monospace',
                        color: AppTheme.accentCyan,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Platform: ${status?.platform.toUpperCase() ?? "UNKNOWN"}',
                      style: const TextStyle(fontSize: 12, color: Colors.white),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Last Scan: ${status?.timestamp.toLocal().toString() ?? "Pending"}',
                      style: const TextStyle(fontSize: 11, color: AppTheme.textMuted),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Deep Probe Cards
            _buildDiagnosticProbe(
              title: 'Root & Privilege Escalation Detector',
              description:
                  'Probes /system/xbin/su, test-keys, Magisk packages, and root execution permissions.',
              isDetected: status?.rootDetected ?? false,
              platformNote: 'Android: Linux /proc/mounts and su binaries.',
            ),
            _buildDiagnosticProbe(
              title: 'Jailbreak & Sandbox Integrity Probe',
              description:
                  'Scans for Cydia/Sileo binaries, MobileSubstrate, and out-of-sandbox file write capabilities.',
              isDetected: status?.jailbreakDetected ?? false,
              platformNote: 'iOS: Mach-O dynamic library loading and sandbox escape tests.',
            ),
            _buildDiagnosticProbe(
              title: 'Virtual Environment / Emulator Check',
              description:
                  'Inspects QEMU pipes, CoreSimulator environment flags, and goldfish/ranchu hardware identifiers.',
              isDetected:
                  (status?.emulatorDetected ?? false) || (status?.simulatorDetected ?? false),
              platformNote: 'Enforces biometric challenge or flags session telemetry.',
            ),
            _buildDiagnosticProbe(
              title: 'Active Debugger / Tracer Probe',
              description:
                  'Queries TracerPid in /proc/self/status, Debug.isDebuggerConnected(), and ptrace(PT_DENY_ATTACH).',
              isDetected: status?.debuggerDetected ?? false,
              platformNote: 'Restricts high-value business operations when active.',
            ),
            _buildDiagnosticProbe(
              title: 'Dynamic Hooking & Frida Scanner',
              description:
                  'Monitors localhost TCP port 27042 and scans memory mappings for frida-agent.so or substrate hooks.',
              isDetected: status?.fridaDetected ?? false,
              platformNote: 'Triggers immediate session revocation in Redis.',
            ),
            _buildDiagnosticProbe(
              title: 'Application Signing Signature Validation',
              description:
                  'Validates SHA-256 APK signing certificate against cryptographic release build digest.',
              isDetected: !(status?.integrityValid ?? true),
              platformNote: 'Defends against modified repackaged APKs/IPAs.',
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDiagnosticProbe({
    required String title,
    required String description,
    required bool isDetected,
    required String platformNote,
  }) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Text(
                    title,
                    style: const TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                ),
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: isDetected
                        ? AppTheme.failRed.withOpacity(0.2)
                        : AppTheme.passGreen.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(6),
                    border: Border.all(
                      color: isDetected ? AppTheme.failRed : AppTheme.passGreen,
                    ),
                  ),
                  child: Text(
                    isDetected ? 'THREAT DETECTED' : 'NOMINAL',
                    style: TextStyle(
                      fontSize: 10,
                      fontWeight: FontWeight.w900,
                      color: isDetected ? AppTheme.failRed : AppTheme.passGreen,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              description,
              style: const TextStyle(fontSize: 12, color: AppTheme.textMuted),
            ),
            const SizedBox(height: 6),
            Text(
              platformNote,
              style: const TextStyle(
                fontSize: 11,
                fontStyle: FontStyle.italic,
                color: Color(0xFF64B5F6),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
