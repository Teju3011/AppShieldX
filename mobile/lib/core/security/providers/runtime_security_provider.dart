import '../models/security_status.dart';

/// Abstract contract for platform-specific runtime protection diagnostics (RASP).
abstract class RuntimeSecurityProvider {
  /// Probes system for root (Android) or jailbreak (iOS) indicators.
  Future<bool> checkRootOrJailbreak();

  /// Detects whether application is executing inside an emulator or simulator.
  Future<bool> checkEmulatorOrSimulator();

  /// Identifies active debugger attachments (ptrace / JDWP / LLDB).
  Future<bool> checkDebuggerAttached();

  /// Scans for dynamic binary instrumentation tools (Frida / Xposed / Substrate).
  Future<bool> checkFridaOrInstrumentation();

  /// Validates application binary signature and package integrity against expected hashes.
  Future<bool> verifyAppIntegrity({String? expectedSignature});

  /// Executes comprehensive audit and aggregates findings into [SecurityStatus].
  Future<SecurityStatus> getSecurityStatus();
}
