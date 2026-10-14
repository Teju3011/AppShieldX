import 'dart:convert';
import 'dart:io' show Platform;
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:uuid/uuid.dart';

String _resolveDefaultPlatform() {
  if (kIsWeb) return 'IOS';
  try {
    return Platform.isIOS ? 'IOS' : 'ANDROID';
  } catch (_) {
    return 'IOS';
  }
}

/// Common Security Event model capturing cross-layer runtime telemetry for Android & iOS.
class SecurityEvent {
  final String id;
  final String? userId;
  final String deviceId;
  final String eventType;
  final String severity; // "LOW", "MEDIUM", "HIGH", "CRITICAL"
  final String source; // "CLIENT_TELEMETRY", "MOBILE_RASP"
  final String description;
  final String? ipAddress;
  final DateTime timestamp;
  final Map<String, dynamic> metadata;
  final String correlationId;

  // Extended Common Security Event Schema fields
  final String platform;
  final String appVersion;
  final double confidence;
  final String? verifiedSessionReference;
  final String endpointCategory;
  final String detectionReason;
  final String verificationStatus;

  SecurityEvent({
    String? id,
    this.userId,
    required this.deviceId,
    required this.eventType,
    required this.severity,
    this.source = 'CLIENT_TELEMETRY',
    required this.description,
    this.ipAddress,
    DateTime? timestamp,
    this.metadata = const {},
    String? correlationId,
    String? platform,
    this.appVersion = '1.0.0',
    this.confidence = 1.0,
    this.verifiedSessionReference,
    this.endpointCategory = 'MOBILE_RASP',
    String? detectionReason,
    this.verificationStatus = 'UNVERIFIED_CLIENT',
  })  : id = id ?? const Uuid().v4(),
        timestamp = timestamp ?? DateTime.now().toUtc(),
        correlationId = correlationId ?? const Uuid().v4(),
        platform = platform ?? _resolveDefaultPlatform(),
        detectionReason = detectionReason ?? description;

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'eventId': id,
      'userId': userId,
      'authenticatedUserReference': userId,
      'deviceId': deviceId,
      'registeredDeviceReference': deviceId,
      'eventType': eventType,
      'severity': severity,
      'source': source,
      'evidenceSource': source,
      'description': description,
      'details': description,
      'ipAddress': ipAddress,
      'timestamp': timestamp.toIso8601String(),
      'eventTimestamp': timestamp.toIso8601String(),
      'platform': platform,
      'appVersion': appVersion,
      'confidence': confidence,
      'verifiedSessionReference': verifiedSessionReference,
      'endpointCategory': endpointCategory,
      'threatCategory': endpointCategory,
      'detectionReason': detectionReason,
      'verificationStatus': verificationStatus,
      'correlationId': correlationId,
      'metadata': metadata,
    };
  }

  factory SecurityEvent.fromMap(Map<String, dynamic> map) {
    return SecurityEvent(
      id: (map['eventId'] ?? map['id']) as String?,
      userId: (map['authenticatedUserReference'] ?? map['userId']) as String?,
      deviceId: (map['registeredDeviceReference'] ?? map['deviceId']) as String? ?? 'unknown-device',
      eventType: map['eventType'] as String? ?? 'UNKNOWN',
      severity: map['severity'] as String? ?? 'LOW',
      source: (map['evidenceSource'] ?? map['source']) as String? ?? 'CLIENT_TELEMETRY',
      description: (map['details'] ?? map['description']) as String? ?? '',
      ipAddress: map['ipAddress'] as String?,
      timestamp: map['eventTimestamp'] != null
          ? DateTime.parse(map['eventTimestamp'] as String)
          : (map['timestamp'] != null ? DateTime.parse(map['timestamp'] as String) : DateTime.now().toUtc()),
      platform: map['platform'] as String?,
      appVersion: map['appVersion'] as String? ?? '1.0.0',
      confidence: (map['confidence'] as num?)?.toDouble() ?? 1.0,
      verifiedSessionReference: map['verifiedSessionReference'] as String?,
      endpointCategory: (map['threatCategory'] ?? map['endpointCategory']) as String? ?? 'MOBILE_RASP',
      detectionReason: (map['detectionReason'] ?? map['description']) as String?,
      verificationStatus: map['verificationStatus'] as String? ?? 'UNVERIFIED_CLIENT',
      correlationId: map['correlationId'] as String?,
      metadata: Map<String, dynamic>.from(map['metadata'] as Map? ?? {}),
    );
  }

  String toJson() => jsonEncode(toMap());

  factory SecurityEvent.fromJson(String source) =>
      SecurityEvent.fromMap(jsonDecode(source) as Map<String, dynamic>);
}
