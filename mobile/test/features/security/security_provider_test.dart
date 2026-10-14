import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_security_reference_app/core/security/models/risk_level.dart';
import 'package:mobile_security_reference_app/core/security/models/security_event.dart';
import 'package:mobile_security_reference_app/core/security/models/security_status.dart';
import 'package:mobile_security_reference_app/features/security/domain/repositories/security_repository.dart';
import 'package:mobile_security_reference_app/features/security/presentation/providers/security_provider.dart';

class MockSecurityRepository implements SecurityRepository {
  SecurityStatus status = SecurityStatus.clean(
    deviceId: 'mock-device-id',
    platform: 'android',
  );
  int offlineCount = 2;

  @override
  Future<SecurityStatus> runSecurityAudit() async {
    return status;
  }

  @override
  Future<SecurityStatus> getLastStatus() async {
    return status;
  }

  @override
  Future<void> reportEvent(SecurityEvent event) async {}

  @override
  Future<SecurityStatus> simulateThreat(String threatType) async {
    status = status.copyWith(
      fridaDetected: threatType == 'FRIDA_DETECTED',
      riskLevel: RiskLevel.critical,
      detectedThreats: [threatType],
    );
    return status;
  }

  @override
  Future<int> flushPendingEvents() async {
    final count = offlineCount;
    offlineCount = 0;
    return count;
  }

  @override
  Future<int> getOfflineQueueCount() async {
    return offlineCount;
  }
}

void main() {
  group('SecurityNotifier State Tests', () {
    late MockSecurityRepository mockRepo;
    late SecurityNotifier notifier;

    setUp(() {
      mockRepo = MockSecurityRepository();
      notifier = SecurityNotifier(mockRepo);
    });

    test('Initial diagnostics populates clean SecurityStatus', () async {
      await notifier.initDiagnostics();
      expect(notifier.state.status?.isCompromised, isFalse);
      expect(notifier.state.status?.riskLevel, equals(RiskLevel.low));
      expect(notifier.state.offlineQueueCount, equals(2));
    });

    test('simulateThreat escalates risk and appends to recent events', () async {
      await notifier.simulateThreat('FRIDA_DETECTED');

      expect(notifier.state.status?.isCompromised, isTrue);
      expect(notifier.state.status?.fridaDetected, isTrue);
      expect(notifier.state.status?.riskLevel, equals(RiskLevel.critical));
      expect(notifier.state.recentEvents.length, equals(1));
      expect(notifier.state.recentEvents.first.eventType, equals('FRIDA_DETECTED'));
    });

    test('flushQueue transmits events and updates offline counter to zero', () async {
      final sent = await notifier.flushQueue();
      expect(sent, equals(2));
      expect(notifier.state.offlineQueueCount, equals(0));
    });
  });
}
