import '../../../../core/security/models/security_event.dart';
import '../../../../core/security/models/security_status.dart';

/// Abstract repository managing security diagnostics, RASP audits, and telemetry reporting.
abstract class SecurityRepository {
  /// Executes a real-time RASP scan across native probes.
  Future<SecurityStatus> runSecurityAudit();

  /// Retrieves the latest known security status.
  Future<SecurityStatus> getLastStatus();

  /// Reports a security incident into the ingestion pipeline.
  Future<void> reportEvent(SecurityEvent event);

  /// Demonstrates framework reaction by injecting a test threat event.
  Future<SecurityStatus> simulateThreat(String threatType);

  /// Synchronizes offline queued telemetry with backend.
  Future<int> flushPendingEvents();

  /// Returns count of pending offline events in local database.
  Future<int> getOfflineQueueCount();
}
