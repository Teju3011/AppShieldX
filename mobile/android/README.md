# Android Native Security Module (Kotlin)

## 1. Architecture Overview

The Android native security module (`android/app/src/main/kotlin/com/framework/security/`) implements high-performance, low-level **Runtime Application Self-Protection (RASP)** probes in native Kotlin, communicating with Flutter via the `MethodChannel` (`com.framework.security/runtime_protection`).

```
                     Flutter Framework Core (Dart)
                                  │
                       MethodChannel Invocations
                                  ▼
           RuntimeProtectionMethodChannelHandler.kt
                                  │
    ┌─────────────────┬───────────┼───────────┬─────────────────┐
    ▼                 ▼           ▼           ▼                 ▼
RootDetector  EmulatorDetector  DebuggerDetector  FridaDetector  IntegrityChecker
```

---

## 2. Implemented Modular Detectors

### 2.1 `RootDetector`
- **SU Binary Paths**: Scans standard partitions (`/system/bin/su`, `/system/xbin/su`, `/sbin/su`, `/data/local/su`).
- **Build Tags**: Evaluates `Build.TAGS` for `test-keys`.
- **Root Management Packages**: Verifies if Magisk, SuperSU, or KingoRoot packages exist.
- **Process Execution**: Attempts to execute `which su`.
- **Mount Verification**: Parses `/proc/mounts` to detect if `/system` or `/` is mounted with `rw` (read-write) privileges.

### 2.2 `EmulatorDetector`
- **Build Properties**: Evaluates `Build.FINGERPRINT`, `Build.MODEL`, `Build.HARDWARE`, `Build.PRODUCT` against goldfish, ranchu, sdk_google, and VirtualBox signatures.
- **QEMU Pipes**: Tests existence of `/dev/socket/qemud` and `/dev/qemu_pipe`.
- **Hypervisor Artifacts**: Detects Genymotion and BlueStacks daemon sockets.

### 2.3 `DebuggerDetector`
- **Android Framework**: Queries `android.os.Debug.isDebuggerConnected()` and `Debug.waitingForDebugger()`.
- **Native TracerPid**: Scans Linux kernel state file `/proc/self/status` for `TracerPid != 0`.
- **Manifest Flags**: Verifies `ApplicationInfo.FLAG_DEBUGGABLE`.

### 2.4 `FridaDetector`
- **Memory Map Inspection**: Audits `/proc/self/maps` looking for loaded dynamic libraries containing `frida`, `gadget`, `libgum`, or `substrate`.
- **TCP Socket Scanner**: Probes default Frida server port `27042` on localhost.
- **Artifacts**: Checks `/data/local/tmp/re.frida.server`.

### 2.5 `IntegrityChecker`
- **APK Signing Certificate**: Computes SHA-256 cryptographic digest of signing certificates via `PackageManager.GET_SIGNING_CERTIFICATES` (API 28+) and compares against reference release digests.

### 2.6 `AndroidSecureStorage`
- **Hardware Keystore**: Implements `MasterKey` with AES-256-GCM encrypted SharedPreferences backed by Android KeyStore.

---

## 3. Window Security Controls

In `MainActivity.kt`, the application applies:
```kotlin
window.setFlags(
    WindowManager.LayoutParams.FLAG_SECURE,
    WindowManager.LayoutParams.FLAG_SECURE
)
```
This prohibits screenshot capture, screen recording, and obscures the app's thumbnail preview in the Android Recent Apps / Task Switcher.

---

## 4. Platform Limitations & Real-World Realities

1. **Kernel-Level Root Hiding (KernelSU / APatch)**:
   - Modern rooting solutions operating in Linux Ring 0 can intercept system calls and spoof `/proc/mounts` or filesystem queries.
2. **Dynamic Frida Port Binding & Cloaking**:
   - Attackers can recompile Frida without string artifacts and bind to random TCP ports.
   - The framework mitigates this via defense-in-depth: client telemetry is verified against server-side risk heuristics at the API Gateway.
