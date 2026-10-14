# iOS Native Security Module (Swift)

## 1. Architecture Overview

The iOS native security module (`ios/Runner/Security/`) provides native Swift implementations of Runtime Application Self-Protection (RASP) probes, hardware Keychain storage, certificate pinning, and background privacy controls.

```
                  Flutter Framework Core (Dart)
                                │
                     MethodChannel Invocations
                                ▼
            RuntimeProtectionMethodChannelHandler.swift
                                │
    ┌─────────────────┬─────────┴─────────┬─────────────────┐
    ▼                 ▼                   ▼                 ▼
JailbreakDetector SimulatorDetector DebuggerDetector FridaDetector
```

---

## 2. Implemented Detectors & Security Controls

### 2.1 `JailbreakDetector`
- **Filesystem Artifacts**: Scans for Cydia, Sileo, Zebra, Substrate, bash, and SSH binaries.
- **Sandbox Escape Test**: Attempts to write and delete a verification token at `/private/jailbreak_sandbox_test.txt`. In a normal sandbox, iOS denies this with `EPERM`.
- **Fork System Call**: Attempts `fork()`. Standard iOS sandboxes forbid process forking; a non-negative PID indicates root/compromised kernel execution.
- **Dyld Loaded Images**: Queries `_dyld_image_count()` to inspect loaded Mach-O images for `MobileSubstrate`, `libhooker`, and `substitute`.

### 2.2 `SimulatorDetector`
- Evaluates `#if targetEnvironment(simulator)` coupled with runtime validation of Xcode `SIMULATOR_DEVICE_NAME` and `hw.machine` sysctl identifiers.

### 2.3 `DebuggerDetector`
- Queries BSD kernel process status using `sysctl` (`CTL_KERN`, `KERN_PROC`, `KERN_PROC_PID`, `getpid()`) to verify whether `p_flag & P_TRACED != 0`.
- Provides dynamic `ptrace(PT_DENY_ATTACH, 0, 0, 0)` support.

### 2.4 `FridaDetector`
- Scans `_dyld_image_name` for `frida`, `gadget`, and `cycript`.
- Resolves exported dynamic symbols (`frida_agent_main`, `gum_init`) via `dlsym`.
- Probes localhost TCP port `27042` via socket connection.

### 2.5 `IntegrityChecker`
- Validates bundle identifier against repackaging and computes SHA-256 digest of main executable Mach-O binary.

### 2.6 `IOSSecureStorage`
- Implements hardware-backed Keychain storage with `kSecClassGenericPassword` and `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly`.

### 2.7 Background Privacy Protection
In `AppDelegate.swift`, `applicationWillResignActive` applies a dark visual blur effect over the entire UI window. This prevents sensitive dashboard credentials, risk badges, or tokens from being saved in the iOS application snapshot switcher thumbnail cache.

---

## 3. iOS Limitations & Academic Rigor

1. **Private Mach APIs**: Apple App Store guidelines forbid calling private kernel APIs (such as `task_for_pid`). Inter-process memory scanning is therefore restricted compared to Android.
2. **Dynamic In-Memory Hooking**: If a jailbreak hook modifies `sysctl` before the app starts, low-level probes can theoretically be hooked. Defense-in-depth ensures server-side API Gateway validation cannot be bypassed.
