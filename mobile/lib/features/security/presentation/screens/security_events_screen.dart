import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../theme/app_theme.dart';
import '../providers/security_provider.dart';

/// Screen displaying captured security telemetry events, correlation IDs, and offline queue status.
class SecurityEventsScreen extends ConsumerWidget {
  const SecurityEventsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final securityState = ref.watch(securityStateProvider);
    final events = securityState.recentEvents;

    return Scaffold(
      appBar: AppBar(
        title: const Text('SECURITY EVENT LOGS'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/dashboard'),
        ),
        actions: [
          if (securityState.offlineQueueCount > 0)
            IconButton(
              icon: const Icon(Icons.cloud_upload_outlined),
              tooltip: 'Flush Offline Queue',
              onPressed: () async {
                final count = await ref
                    .read(securityStateProvider.notifier)
                    .flushQueue();
                if (context.mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text('Dispatched $count events to API Gateway.'),
                      backgroundColor: AppTheme.passGreen,
                    ),
                  );
                }
              },
            ),
        ],
      ),
      body: events.isEmpty
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.verified_user_outlined,
                      size: 64, color: AppTheme.passGreen),
                  const SizedBox(height: 16),
                  const Text(
                    'Zero Active Threat Incidents',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'No security events recorded in local queue or backend stream.',
                    style: TextStyle(fontSize: 12, color: AppTheme.textMuted),
                  ),
                  const SizedBox(height: 24),
                  ElevatedButton(
                    onPressed: () {
                      ref
                          .read(securityStateProvider.notifier)
                          .simulateThreat('DEBUGGER_DETECTED');
                    },
                    child: const Text('Simulate Test Incident'),
                  ),
                ],
              ),
            )
          : ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: events.length,
              itemBuilder: (context, index) {
                final event = events[index];
                final Color color = event.severity == 'CRITICAL'
                    ? AppTheme.criticalPurple
                    : event.severity == 'HIGH'
                        ? AppTheme.failRed
                        : AppTheme.warningAmber;

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
                            Text(
                              event.eventType,
                              style: const TextStyle(
                                fontSize: 14,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            ),
                            Container(
                              padding: const EdgeInsets.symmetric(
                                  horizontal: 8, vertical: 3),
                              decoration: BoxDecoration(
                                color: color.withOpacity(0.15),
                                borderRadius: BorderRadius.circular(6),
                                border: Border.all(color: color),
                              ),
                              child: Text(
                                event.severity,
                                style: TextStyle(
                                  fontSize: 10,
                                  fontWeight: FontWeight.bold,
                                  color: color,
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(
                          event.description,
                          style: const TextStyle(
                              fontSize: 12, color: Colors.white70),
                        ),
                        const SizedBox(height: 12),
                        const Divider(color: Color(0xFF2E4057), height: 1),
                        const SizedBox(height: 8),
                        Text(
                          'X-Correlation-ID: ${event.correlationId}',
                          style: const TextStyle(
                            fontSize: 10,
                            fontFamily: 'monospace',
                            color: AppTheme.textMuted,
                          ),
                        ),
                        Text(
                          'Device ID: ${event.deviceId}',
                          style: const TextStyle(
                            fontSize: 10,
                            fontFamily: 'monospace',
                            color: AppTheme.textMuted,
                          ),
                        ),
                        Text(
                          'Timestamp (UTC): ${event.timestamp.toIso8601String()}',
                          style: const TextStyle(
                            fontSize: 10,
                            fontFamily: 'monospace',
                            color: AppTheme.textMuted,
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }
}
