import '../models/security_event.dart';

/// Abstract contract for reporting telemetry events to the Cloud Threat Detection engine.
abstract class SecurityEventReporter {
  /// Reports a single security event, queuing locally if offline.
  Future<void> reportEvent(SecurityEvent event);

  /// Synchronously or periodically flushes queued events to the backend.
  /// Returns the count of successfully transmitted events.
  Future<int> flushQueue();

  /// Gets total count of pending un-transmitted events stored locally.
  Future<int> getPendingQueueCount();
}
