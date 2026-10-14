import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';

/// Advanced Healthcare & Clinical EHR Portal View
/// Demonstrates cross-domain reusability of the AppShieldX framework for HIPAA/GDPR compliance,
/// protecting Electronic Protected Health Information (ePHI) from runtime tampering.
class AdvancedHealthcareView extends StatefulWidget {
  final dynamic securityStatus;

  const AdvancedHealthcareView({super.key, required this.securityStatus});

  @override
  State<AdvancedHealthcareView> createState() => _AdvancedHealthcareViewState();
}

class _AdvancedHealthcareViewState extends State<AdvancedHealthcareView> {
  int _selectedPatientIndex = 0;
  bool _isAuthorizing = false;

  final List<Map<String, dynamic>> _patients = [
    {
      'name': 'Eleanor Vance',
      'id': 'EHR-94021',
      'age': 42,
      'gender': 'Female',
      'blood': 'A+',
      'ward': 'Cardiology & Oncology • Bed 4B',
      'primaryDiagnosis': 'Hypertension Stage 2 • Post-Chemotherapy Monitoring',
      'hr': '72 BPM',
      'spo2': '98%',
      'bp': '118/76',
      'temp': '98.4 °F',
      'medication': 'Oxycodone 20mg IV • Q6H PRN Pain',
    },
    {
      'name': 'Marcus Brody',
      'id': 'EHR-77192',
      'age': 58,
      'gender': 'Male',
      'blood': 'O-',
      'ward': 'Intensive Care Unit (ICU) • Pod 2',
      'primaryDiagnosis': 'Acute Coronary Syndrome • Post-Angioplasty Day 1',
      'hr': '94 BPM',
      'spo2': '94%',
      'bp': '142/90',
      'temp': '99.1 °F',
      'medication': 'Heparin Sodium Infusion • 18 units/kg/hr',
    },
    {
      'name': 'Sophia Chen',
      'id': 'EHR-33810',
      'age': 27,
      'gender': 'Female',
      'blood': 'B+',
      'ward': 'Emergency Trauma Center • Bay 1',
      'primaryDiagnosis': 'Closed Head Trauma • GCS 14 Alert',
      'hr': '82 BPM',
      'spo2': '99%',
      'bp': '124/80',
      'temp': '98.6 °F',
      'medication': 'Mannitol 20% IV Infusion • 1g/kg',
    },
  ];

  void _authorizeMedication() {
    final status = widget.securityStatus;
    final bool isCompromised = (status?.rootDetected ?? false) ||
        (status?.jailbreakDetected ?? false) ||
        (status?.fridaDetected ?? false) ||
        (status?.debuggerDetected ?? false) ||
        (status?.riskLevel.toProtocolString() == 'CRITICAL');

    setState(() => _isAuthorizing = true);

    Future.delayed(const Duration(milliseconds: 700), () {
      if (!mounted) return;
      setState(() => _isAuthorizing = false);

      final curPatient = _patients[_selectedPatientIndex];

      if (isCompromised) {
        showDialog(
          context: context,
          builder: (ctx) => AlertDialog(
            backgroundColor: const Color(0xFF161F30),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
              side: const BorderSide(color: AppTheme.failRed, width: 2),
            ),
            title: const Row(
              children: [
                Icon(Icons.gpp_bad, color: AppTheme.failRed, size: 28),
                SizedBox(width: 10),
                Text(
                  'HIPAA ePHI ACCESS BLOCKED',
                  style: TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.bold,
                    color: AppTheme.failRed,
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
                  child: const Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text('ENFORCEMENT:',
                          style: TextStyle(
                              fontSize: 11, fontWeight: FontWeight.bold)),
                      Text('ZERO-TRUST QUARANTINE',
                          style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.bold,
                              color: AppTheme.failRed)),
                    ],
                  ),
                ),
                const SizedBox(height: 12),
                Text(
                  'Prescription dispensation for ${curPatient['name']} (${curPatient['medication']}) was terminated by AppShieldX.\n\nReason: Kernel root / memory hooking (Frida/Magisk) detected on clinician handheld. To prevent lethal dosage alteration or medical record fraud, access is locked.',
                  style: const TextStyle(fontSize: 12, height: 1.4),
                ),
                const SizedBox(height: 12),
                const Text(
                  'Regulatory Non-Compliance Alert Dispatched:\n• Audit Log committed to AWS CloudWatch & S3\n• Incident flagged under HIPAA Security Rule §164.312',
                  style: TextStyle(fontSize: 11, color: AppTheme.textMuted),
                ),
              ],
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(ctx),
                child: const Text('DISMISS',
                    style: TextStyle(color: AppTheme.accentCyan)),
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
                  'PRESCRIPTION ATTESTED',
                  style: TextStyle(
                    fontSize: 15,
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
                  'Medication order approved for ${curPatient['name']}.\nRx: ${curPatient['medication']}',
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
                      Text('CLINICIAN CRYPTOGRAPHIC SIGNATURE:',
                          style: TextStyle(
                              fontSize: 9,
                              fontWeight: FontWeight.bold,
                              color: AppTheme.accentCyan)),
                      SizedBox(height: 4),
                      Text('Dr. Gregory House, MD • DEA: BB9412049',
                          style: TextStyle(fontSize: 11, color: Colors.white70)),
                      SizedBox(height: 6),
                      Text('HARDWARE ATTESTATION HASH:',
                          style: TextStyle(
                              fontSize: 9,
                              fontWeight: FontWeight.bold,
                              color: AppTheme.accentCyan)),
                      SizedBox(height: 4),
                      Text('SHA256: 3c7a81b...f942 (FIDO2 L2 KeyStore Valid)',
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
                child: const Text('CONFIRM',
                    style: TextStyle(color: AppTheme.passGreen)),
              ),
            ],
          ),
        );
      }
    });
  }

  void _triggerBreakGlassOverride() {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF161F30),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: const BorderSide(color: AppTheme.warningAmber, width: 2),
        ),
        title: const Row(
          children: [
            Icon(Icons.warning_amber, color: AppTheme.warningAmber, size: 28),
            SizedBox(width: 10),
            Text(
              'BREAK-GLASS PROTOCOL',
              style: TextStyle(
                fontSize: 15,
                fontWeight: FontWeight.bold,
                color: AppTheme.warningAmber,
              ),
            ),
          ],
        ),
        content: const Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'EMERGENCY TRAUMA ACCESS INVOKED\n\nIn accordance with HIPAA §164.312(a)(2)(ii), emergency override bypasses standard authorization barriers for life-threatening patient care.',
              style: TextStyle(fontSize: 12, height: 1.4),
            ),
            SizedBox(height: 12),
            Text(
              'Mandatory Telemetry Dispatched:\n• Cryptographic audit event logged to AWS CloudWatch\n• Incident broadcast to SOC Admin Dashboard\n• 72-hour clinical retrospective review initiated',
              style: TextStyle(fontSize: 11, color: AppTheme.textMuted),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('ACKNOWLEDGE & DISPATCH AUDIT',
                style: TextStyle(color: AppTheme.warningAmber)),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final curPatient = _patients[_selectedPatientIndex];
    final status = widget.securityStatus;
    final bool isCompromised = (status?.rootDetected ?? false) ||
        (status?.jailbreakDetected ?? false) ||
        (status?.fridaDetected ?? false) ||
        (status?.debuggerDetected ?? false) ||
        (status?.riskLevel.toProtocolString() == 'CRITICAL');

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // Patient Selector Header
        Card(
          color: const Color(0xFF161B26),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
            side: const BorderSide(color: Color(0xFF283548)),
          ),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    const Icon(Icons.local_hospital,
                        color: Color(0xFF60A5FA), size: 22),
                    const SizedBox(width: 8),
                    const Expanded(
                      child: Text(
                        'CLINICAL PATIENT RECORD (EHR)',
                        style: TextStyle(
                          fontSize: 13,
                          fontWeight: FontWeight.bold,
                          letterSpacing: 0.8,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    const SizedBox(width: 8),
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(
                        color: const Color(0xFF60A5FA).withOpacity(0.15),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: const Text('HL7 / FHIR v4',
                          style: TextStyle(
                              fontSize: 10,
                              fontWeight: FontWeight.bold,
                              color: Color(0xFF60A5FA))),
                    ),
                  ],
                ),
                const SizedBox(height: 12),

                // Patient Chips
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: List.generate(_patients.length, (i) {
                      final isSelected = _selectedPatientIndex == i;
                      final p = _patients[i];
                      return Padding(
                        padding: const EdgeInsets.only(right: 8),
                        child: ChoiceChip(
                          label: Text('${p['name']} (${p['id']})'),
                          selected: isSelected,
                          selectedColor: const Color(0xFF2563EB),
                          backgroundColor: const Color(0xFF1E283D),
                          labelStyle: TextStyle(
                            color: isSelected ? Colors.white : Colors.white70,
                            fontWeight: isSelected
                                ? FontWeight.bold
                                : FontWeight.normal,
                            fontSize: 11,
                          ),
                          onSelected: (val) {
                            if (val) setState(() => _selectedPatientIndex = i);
                          },
                        ),
                      );
                    }),
                  ),
                ),
                const Divider(color: Color(0xFF283548), height: 24),

                // Selected Patient Overview
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          curPatient['name'] as String,
                          style: const TextStyle(
                              fontSize: 18, fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          'Age: ${curPatient['age']} • ${curPatient['gender']} • Blood: ${curPatient['blood']}',
                          style: const TextStyle(
                              fontSize: 11, color: AppTheme.textMuted),
                        ),
                      ],
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: AppTheme.warningAmber.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(6),
                        border: Border.all(
                            color: AppTheme.warningAmber.withOpacity(0.5)),
                      ),
                      child: const Text(
                        'CONFIDENTIAL ePHI',
                        style: TextStyle(
                          fontSize: 9,
                          fontWeight: FontWeight.bold,
                          color: AppTheme.warningAmber,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Text(
                  'Ward: ${curPatient['ward']}',
                  style: const TextStyle(fontSize: 11, color: Colors.white70),
                ),
                const SizedBox(height: 4),
                Text(
                  'Diagnosis: ${curPatient['primaryDiagnosis']}',
                  style: const TextStyle(fontSize: 11, color: Color(0xFF93C5FD)),
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),

        // Live Vital Signs Grid
        Row(
          children: [
            _buildVitalCard('HEART RATE', curPatient['hr'] as String,
                Icons.favorite, AppTheme.failRed),
            const SizedBox(width: 8),
            _buildVitalCard('OXYGEN (SpO2)', curPatient['spo2'] as String,
                Icons.air, const Color(0xFF60A5FA)),
            const SizedBox(width: 8),
            _buildVitalCard('BLOOD PRESSURE', curPatient['bp'] as String,
                Icons.speed, AppTheme.passGreen),
            const SizedBox(width: 8),
            _buildVitalCard('TEMPERATURE', curPatient['temp'] as String,
                Icons.thermostat, AppTheme.warningAmber),
          ],
        ),
        const SizedBox(height: 16),

        // Prescription & Action Console
        Card(
          color: const Color(0xFF161B26),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
            side: const BorderSide(color: Color(0xFF283548)),
          ),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'HIGH-RISK CLINICAL INTERVENTION CONSOLE:',
                  style: TextStyle(
                    fontSize: 11,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1,
                    color: AppTheme.textMuted,
                  ),
                ),
                const SizedBox(height: 12),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: const Color(0xFF0F1523),
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: const Color(0xFF283548)),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text('SCHEDULED MEDICATION ORDER:',
                              style: TextStyle(
                                  fontSize: 9,
                                  fontWeight: FontWeight.bold,
                                  color: AppTheme.textMuted)),
                          const SizedBox(height: 3),
                          Text(
                            curPatient['medication'] as String,
                            style: const TextStyle(
                                fontSize: 13,
                                fontWeight: FontWeight.bold,
                                color: Colors.white),
                          ),
                        ],
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 8, vertical: 3),
                        decoration: BoxDecoration(
                          color: AppTheme.failRed.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: const Text('SCHEDULE II',
                            style: TextStyle(
                                fontSize: 9,
                                fontWeight: FontWeight.bold,
                                color: AppTheme.failRed)),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 16),

                // Authorize Button
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    icon: _isAuthorizing
                        ? const SizedBox(
                            width: 18,
                            height: 18,
                            child: CircularProgressIndicator(
                              strokeWidth: 2,
                              color: Colors.white,
                            ),
                          )
                        : Icon(
                            isCompromised
                                ? Icons.lock
                                : Icons.assignment_turned_in,
                            size: 18,
                          ),
                    label: Text(
                      _isAuthorizing
                          ? 'VERIFYING DOCTOR ATTESTATION...'
                          : (isCompromised
                              ? 'DISPENSATION BLOCKED (RASP QUARANTINE)'
                              : 'AUTHORIZE CONTROLLED PRESCRIPTION'),
                    ),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: isCompromised
                          ? AppTheme.failRed
                          : const Color(0xFF2563EB),
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10),
                      ),
                    ),
                    onPressed: _isAuthorizing ? null : _authorizeMedication,
                  ),
                ),
                const SizedBox(height: 10),

                // Break-Glass Button
                SizedBox(
                  width: double.infinity,
                  child: OutlinedButton.icon(
                    icon: const Icon(Icons.emergency,
                        color: AppTheme.warningAmber, size: 18),
                    label: const Text(
                      'EMERGENCY BREAK-GLASS OVERRIDE (DISPATCH AUDIT)',
                      style: TextStyle(color: AppTheme.warningAmber, fontSize: 11),
                    ),
                    style: OutlinedButton.styleFrom(
                      side: const BorderSide(color: AppTheme.warningAmber),
                      padding: const EdgeInsets.symmetric(vertical: 12),
                    ),
                    onPressed: _triggerBreakGlassOverride,
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildVitalCard(
      String label, String value, IconData icon, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 8),
        decoration: BoxDecoration(
          color: const Color(0xFF161B26),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: const Color(0xFF283548)),
        ),
        child: Column(
          children: [
            Icon(icon, color: color, size: 18),
            const SizedBox(height: 6),
            Text(
              value,
              style: const TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w900,
                color: Colors.white,
              ),
            ),
            const SizedBox(height: 2),
            Text(
              label,
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 8,
                fontWeight: FontWeight.bold,
                color: AppTheme.textMuted,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
