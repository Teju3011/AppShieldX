import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/security/models/security_event.dart';
import '../../../../core/security/models/security_status.dart';
import '../../domain/repositories/security_repository.dart';

/// State representation for live device security status and telemetry.
class SecurityState {
  final bool isScanning;
  final SecurityStatus? status;
  final int offlineQueueCount;
  final List<SecurityEvent> recentEvents;
  final String? errorMessage;

  const SecurityState({
    this.isScanning = false,
    this.status,
    this.offlineQueueCount = 0,
    this.recentEvents = const [],
    this.errorMessage,
  });

  SecurityState copyWith({
    bool? isScanning,
    SecurityStatus? status,
    int? offlineQueueCount,
    List<SecurityEvent>? recentEvents,
    String? errorMessage,
  }) {
    return SecurityState(
      isScanning: isScanning ?? this.isScanning,
      status: status ?? this.status,
      offlineQueueCount: offlineQueueCount ?? this.offlineQueueCount,
      recentEvents: recentEvents ?? this.recentEvents,
      errorMessage: errorMessage,
    );
  }
}

/// Provider orchestrating RASP diagnostics, event queues, and threat simulations.
class SecurityNotifier extends StateNotifier<SecurityState> {
  final SecurityRepository _repository;

  SecurityNotifier(this._repository) : super(const SecurityState()) {
    initDiagnostics();
  }

  Future<void> initDiagnostics() async {
    state = state.copyWith(isScanning: true, errorMessage: null);
    try {
      final status = await _repository.runSecurityAudit();
      final count = await _repository.getOfflineQueueCount();
      state = state.copyWith(
        isScanning: false,
        status: status,
        offlineQueueCount: count,
      );
    } catch (e) {
      state = state.copyWith(isScanning: false, errorMessage: e.toString());
    }
  }

  Future<void> scanRuntimeSecurity() async {
    state = state.copyWith(isScanning: true, errorMessage: null);
    try {
      final status = await _repository.runSecurityAudit();
      final count = await _repository.getOfflineQueueCount();
      state = state.copyWith(
        isScanning: false,
        status: status,
        offlineQueueCount: count,
      );
    } catch (e) {
      state = state.copyWith(isScanning: false, errorMessage: e.toString());
    }
  }

  Future<void> simulateThreat(String threatType) async {
    state = state.copyWith(isScanning: true);
    try {
      final updatedStatus = await _repository.simulateThreat(threatType);
      final count = await _repository.getOfflineQueueCount();

      // Add to local recent events list for immediate UI display
      final newEvent = SecurityEvent(
        deviceId: updatedStatus.deviceId,
        eventType: threatType,
        severity: updatedStatus.riskLevel.toProtocolString(),
        source: 'MOBILE_RASP',
        description: 'Simulated runtime detection: $threatType',
      );

      final updatedEvents = [newEvent, ...state.recentEvents];

      state = state.copyWith(
        isScanning: false,
        status: updatedStatus,
        offlineQueueCount: count,
        recentEvents: updatedEvents.take(10).toList(),
      );
    } catch (e) {
      state = state.copyWith(isScanning: false, errorMessage: e.toString());
    }
  }

  Future<int> flushQueue() async {
    try {
      final count = await _repository.flushPendingEvents();
      final remaining = await _repository.getOfflineQueueCount();
      state = state.copyWith(offlineQueueCount: remaining);
      return count;
    } catch (_) {
      return 0;
    }
  }
}

final securityRepositoryProvider = Provider<SecurityRepository>((ref) {
  throw UnimplementedError('securityRepositoryProvider must be initialized in main');
});

final securityStateProvider =
    StateNotifierProvider<SecurityNotifier, SecurityState>((ref) {
  final repository = ref.watch(securityRepositoryProvider);
  return SecurityNotifier(repository);
});
