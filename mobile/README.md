# Mobile Security Framework (Core & Reference Implementation)

## 1. Overview

The `mobile/` module houses both the **Reusable Mobile Security Framework** (`lib/core/`) and the reference application **SecureApp** (`lib/features/`).

The framework guarantees:
1. **Runtime Application Self-Protection (RASP)**: Proactive runtime probes auditing root, jailbreak, emulator, debugger, and Frida injection.
2. **Hardware-Backed Secure Storage**: AES-256 encrypted credential management via Android Keystore and iOS Keychain.
3. **Resilient Offline Telemetry Queue**: Encrypted SQLite buffering ensuring zero security event data loss during network disconnections.
4. **Zero-Trust Network Client**: TLS 1.3 certificate/public-key pinning, automated correlation ID injection, and transparent token rotation.

---

## 2. Framework Folder Structure

```
mobile/
├── android/                   # Native Android Kotlin Security Modules (Phase 4)
├── ios/                       # Native iOS Swift Security Modules (Phase 5)
├── lib/
│   ├── core/
│   │   ├── config/            # SecurityConfig, AppConfig
│   │   ├── constants/         # ApiConstants, SecurityConstants
│   │   ├── error/             # Exceptions, Failures
│   │   ├── network/           # ApiClient, Interceptors (Auth, Correlation, Refresh, Error)
│   │   ├── security/          # Models (SecurityStatus, Event, RiskLevel) & Providers
│   │   ├── storage/           # TokenManager
│   │   └── utils/             # DeviceFingerprint, SecurityLogger
│   ├── features/              # Reference SecureApp UI (Phase 3)
│   └── main.dart              # Entry Point (Phase 3)
├── test/
│   └── core/                  # Security Status, Risk Engine, and Storage Tests
└── pubspec.yaml               # Dependencies & Manifest
```

---

## 3. Integration Example

Any third-party Flutter application can consume the security framework:
```dart
import 'package:mobile_security_reference_app/core/security/security_framework.dart';
import 'package:mobile_security_reference_app/core/config/security_config.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize Security Framework with custom policies
  final framework = await SecurityFramework.initialize(
    config: SecurityConfig.production(
      pinnedCertificatesSHA256: ['sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='],
    ),
  );

  // Perform Pre-flight RASP audit
  final status = await framework.checkRuntimeSecurity();
  if (status.riskLevel == RiskLevel.critical) {
    // Terminate or display security advisory
    return;
  }

  // Create Pinned API Client
  final client = framework.createSecureApiClient(
    baseUrl: 'https://gateway.enterprise.io:8080',
  );

  runApp(MyApp(client: client));
}
```

---

## 4. Verification & Testing

Run Dart unit tests:
```bash
flutter test test/core/
```
