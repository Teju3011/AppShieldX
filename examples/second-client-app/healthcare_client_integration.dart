// =============================================================================
// AppShieldX Integration Example: HealthcarePortalClient (Sample 2nd Application)
// Demonstrates seamless reuse of AppShieldX Mobile Security Framework without
// modifying the backend correlation engine.
// =============================================================================

import 'package:flutter/material.dart';

// 1. IMPORT REUSABLE APPSHIELDX SECURITY FRAMEWORK MODULES
// In a standalone app, this is packaged as an internal Flutter package / pub dependency:
// import 'package:appshieldx_mobile_sdk/appshieldx.dart';

abstract class AppShieldXClientSdk {
  static Future<void> initialize({
    required String apiGatewayUrl,
    required String appVersion,
    required Function(Map<String, dynamic> riskStatus) onRiskPolicyEvaluated,
  }) async {
    // Initializes Keystore/Keychain, background RASP probes, offline SQLite queue,
    // and attaches dynamic headers (X-Device-ID, X-Correlation-ID).
    debugPrint('[AppShieldX SDK] Initialized for HealthcarePortal v$appVersion at $apiGatewayUrl');
  }

  static Future<void> submitRuntimeTelemetry({
    required String eventType,
    required String severity,
    required String reason,
    double confidence = 1.0,
  }) async {
    // Encapsulates Common Security Event Schema serialization
    final eventPayload = {
      'eventType': eventType,
      'severity': severity,
      'confidence': confidence,
      'endpointCategory': 'HEALTHCARE_RECORDS_ACCESS',
      'detectionReason': reason,
      'platform': 'ANDROID', // Autodetected at runtime
      'evidenceSource': 'CLIENT_TELEMETRY',
      'timestamp': DateTime.now().toUtc().toIso8601String(),
    };
    debugPrint('[AppShieldX SDK] Dispatching Common Security Event: $eventPayload');
  }
}

// 2. SAMPLE HEALTHCARE APPLICATION USING APPSHIELDX SDK
class HealthcarePortalApp extends StatefulWidget {
  const HealthcarePortalApp({super.key});

  @override
  State<HealthcarePortalApp> createState() => _HealthcarePortalAppState();
}

class _HealthcarePortalAppState extends State<HealthcarePortalApp> {
  String _riskBand = 'ALLOW';

  @override
  void initState() {
    super.initState();
    // Step 1: Initialize AppShieldX SDK on App Launch (3 lines of code)
    AppShieldXClientSdk.initialize(
      apiGatewayUrl: 'https://gateway.healthcare.internal:8080',
      appVersion: '2.1.0',
      onRiskPolicyEvaluated: (status) {
        setState(() {
          _riskBand = status['responseBand'] ?? 'ALLOW';
        });
      },
    );
  }

  // Step 2: Sample Protected Action (e.g., Access Electronic Health Record)
  Future<void> _viewPatientHealthRecord(String patientId) async {
    if (_riskBand == 'RESTRICT_SENSITIVE_ACTIONS') {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Access Blocked: Zero-Trust Policy restricted state-modifying actions.'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    // Step 3: Trigger runtime integrity check opportunistically before viewing records
    await AppShieldXClientSdk.submitRuntimeTelemetry(
      eventType: 'INTEGRITY_VERIFICATION_PASS',
      severity: 'INFO',
      reason: 'Routine pre-transaction memory and package certificate verification',
    );

    debugPrint('Successfully queried EHR for patient: $patientId');
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('Healthcare EHR Portal')),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('Active Security Posture Band: $_riskBand'),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: () => _viewPatientHealthRecord('PT-99023'),
                child: const Text('View Patient Record (PT-99023)'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
