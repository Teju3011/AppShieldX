import 'package:dio/dio.dart';
import '../../constants/api_constants.dart';
import '../models/security_event.dart';
import 'offline_security_event_queue.dart';
import 'security_event_reporter.dart';

/// Implementation of [SecurityEventReporter] with resilient offline buffering and auto-sync.
class SecurityEventReporterImpl implements SecurityEventReporter {
  final Dio _dio;
  final OfflineSecurityEventQueue _queue;
  bool _isFlushing = false;

  SecurityEventReporterImpl({
    required Dio dio,
    OfflineSecurityEventQueue? queue,
  })  : _dio = dio,
        _queue = queue ?? OfflineSecurityEventQueue();

  @override
  Future<void> reportEvent(SecurityEvent event) async {
    // 1. Persist immediately to resilient local SQLite queue
    await _queue.enqueue(event);

    // 2. Attempt opportunistic background dispatch
    unawaited(_triggerFlush());
  }

  @override
  Future<int> flushQueue() async {
    return await _triggerFlush();
  }

  @override
  Future<int> getPendingQueueCount() async {
    return await _queue.countPending();
  }

  Future<int> _triggerFlush() async {
    if (_isFlushing) return 0;
    _isFlushing = true;

    int totalSent = 0;
    try {
      final List<SecurityEvent> pending = await _queue.getPendingEvents();
      if (pending.isEmpty) return 0;

      for (final event in pending) {
        try {
          final response = await _dio.post(
            ApiConstants.securityEventsEndpoint,
            data: event.toMap(),
            options: Options(
              headers: {
                'X-Correlation-ID': event.correlationId,
                'X-Device-ID': event.deviceId,
              },
            ),
          );

          if (response.statusCode == 200 ||
              response.statusCode == 201 ||
              response.statusCode == 202) {
            await _queue.markSubmitted([event.id]);
            totalSent++;
          } else {
            await _queue.recordFailure([event.id]);
          }
        } catch (_) {
          // Network drop; abort batch and retain pending events for next retry cycle
          await _queue.recordFailure([event.id]);
          break;
        }
      }
    } finally {
      _isFlushing = false;
    }

    return totalSent;
  }
}

void unawaited(Future<void> future) {}
