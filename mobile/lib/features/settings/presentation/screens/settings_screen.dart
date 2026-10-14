import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../../../theme/app_theme.dart';

/// Settings screen for configuring runtime protection policies and API endpoints.
class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool _rootDetection = true;
  bool _emulatorDetection = true;
  bool _debuggerDetection = true;
  bool _fridaDetection = true;
  bool _tlsPinning = true;
  bool _biometrics = true;
  bool _eventReporting = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('FRAMEWORK SETTINGS'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/dashboard'),
        ),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const Text(
            'RUNTIME PROTECTION MODULES (RASP)',
            style: TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.bold,
              color: AppTheme.textMuted,
            ),
          ),
          const SizedBox(height: 8),
          Card(
            child: Column(
              children: [
                SwitchListTile(
                  title: const Text('Root & Jailbreak Detection'),
                  subtitle: const Text('Checks /system binaries, Cydia, test-keys'),
                  value: _rootDetection,
                  activeColor: AppTheme.accentCyan,
                  onChanged: (val) => setState(() => _rootDetection = val),
                ),
                const Divider(color: Color(0xFF2E4057), height: 1),
                SwitchListTile(
                  title: const Text('Emulator & Simulator Detection'),
                  subtitle: const Text('Probes QEMU pipes and build properties'),
                  value: _emulatorDetection,
                  activeColor: AppTheme.accentCyan,
                  onChanged: (val) => setState(() => _emulatorDetection = val),
                ),
                const Divider(color: Color(0xFF2E4057), height: 1),
                SwitchListTile(
                  title: const Text('Active Debugger Detection'),
                  subtitle: const Text('Monitors TracerPid and ptrace attachments'),
                  value: _debuggerDetection,
                  activeColor: AppTheme.accentCyan,
                  onChanged: (val) => setState(() => _debuggerDetection = val),
                ),
                const Divider(color: Color(0xFF2E4057), height: 1),
                SwitchListTile(
                  title: const Text('Dynamic Hooking / Frida Scanner'),
                  subtitle: const Text('Scans port 27042 and frida-agent.so libraries'),
                  value: _fridaDetection,
                  activeColor: AppTheme.accentCyan,
                  onChanged: (val) => setState(() => _fridaDetection = val),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          const Text(
            'TRANSPORT & PERSISTENCE SECURITY',
            style: TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.bold,
              color: AppTheme.textMuted,
            ),
          ),
          const SizedBox(height: 8),
          Card(
            child: Column(
              children: [
                SwitchListTile(
                  title: const Text('TLS Certificate / Public Key Pinning'),
                  subtitle: const Text('Enforces SPKI SHA-256 fingerprint verification'),
                  value: _tlsPinning,
                  activeColor: AppTheme.accentCyan,
                  onChanged: (val) => setState(() => _tlsPinning = val),
                ),
                const Divider(color: Color(0xFF2E4057), height: 1),
                SwitchListTile(
                  title: const Text('Biometric Quick Authentication'),
                  subtitle: const Text('Android BiometricPrompt & iOS LocalAuthentication'),
                  value: _biometrics,
                  activeColor: AppTheme.accentCyan,
                  onChanged: (val) => setState(() => _biometrics = val),
                ),
                const Divider(color: Color(0xFF2E4057), height: 1),
                SwitchListTile(
                  title: const Text('Real-Time Security Event Telemetry'),
                  subtitle: const Text('Streams RASP violation alerts to Cloud Threat Service'),
                  value: _eventReporting,
                  activeColor: AppTheme.accentCyan,
                  onChanged: (val) => setState(() => _eventReporting = val),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          Card(
            child: ListTile(
              leading: const Icon(Icons.info_outline, color: AppTheme.accentCyan),
              title: const Text('About Framework Architecture'),
              subtitle: const Text('B.Tech Project Specifications & Module Overview'),
              trailing: const Icon(Icons.chevron_right),
              onTap: () => context.go('/about'),
            ),
          ),
        ],
      ),
    );
  }
}
