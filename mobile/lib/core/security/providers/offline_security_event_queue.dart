import 'dart:async';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';
import '../../constants/security_constants.dart';
import '../models/security_event.dart';

/// SQLite-backed resilient queue buffering security events when the device is disconnected.
class OfflineSecurityEventQueue {
  static const String _tableName = 'offline_security_events';
  Database? _database;
  final List<SecurityEvent> _webInMemoryQueue = [];

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    final String databasesPath = await getDatabasesPath();
    final String path = join(databasesPath, 'security_telemetry_queue.db');

    return await openDatabase(
      path,
      version: 1,
      onCreate: (Database db, int version) async {
        await db.execute('''
          CREATE TABLE $_tableName (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            device_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            source TEXT NOT NULL,
            description TEXT NOT NULL,
            ip_address TEXT,
            timestamp TEXT NOT NULL,
            metadata TEXT NOT NULL,
            correlation_id TEXT NOT NULL,
            submitted INTEGER NOT NULL DEFAULT 0,
            retry_count INTEGER NOT NULL DEFAULT 0,
            created_at INTEGER NOT NULL
          )
        ''');

        await db.execute(
            'CREATE INDEX idx_queue_submitted ON $_tableName(submitted, created_at)');
      },
    );
  }

  /// Inserts a new event into the local queue.
  Future<void> enqueue(SecurityEvent event) async {
    if (kIsWeb) {
      _webInMemoryQueue.add(event);
      if (_webInMemoryQueue.length > SecurityConstants.maxOfflineEvents) {
        _webInMemoryQueue.removeAt(0);
      }
      return;
    }

    final Database db = await database;
    await db.insert(
      _tableName,
      {
        'id': event.id,
        'user_id': event.userId,
        'device_id': event.deviceId,
        'event_type': event.eventType,
        'severity': event.severity,
        'source': event.source,
        'description': event.description,
        'ip_address': event.ipAddress,
        'timestamp': event.timestamp.toIso8601String(),
        'metadata': event.toJson(), // store serialized event
        'correlation_id': event.correlationId,
        'submitted': 0,
        'retry_count': 0,
        'created_at': DateTime.now().millisecondsSinceEpoch,
      },
      conflictAlgorithm: ConflictAlgorithm.replace,
    );

    // Enforce max capacity cap to avoid disk saturation
    await _enforceCapacity();
  }

  /// Retrieves up to [limit] un-submitted events ordered by timestamp.
  Future<List<SecurityEvent>> getPendingEvents({int limit = SecurityConstants.batchUploadSize}) async {
    if (kIsWeb) {
      return _webInMemoryQueue.take(limit).toList();
    }

    final Database db = await database;
    final List<Map<String, dynamic>> maps = await db.query(
      _tableName,
      where: 'submitted = ?',
      whereArgs: [0],
      orderBy: 'created_at ASC',
      limit: limit,
    );

    return maps.map((row) {
      final String rawMetadata = row['metadata'] as String;
      return SecurityEvent.fromJson(rawMetadata);
    }).toList();
  }

  /// Marks a batch of successfully transmitted event IDs to prevent duplicate transmission.
  Future<void> markSubmitted(List<String> eventIds) async {
    if (eventIds.isEmpty) return;
    if (kIsWeb) {
      _webInMemoryQueue.removeWhere((e) => eventIds.contains(e.id));
      return;
    }

    final Database db = await database;
    final String inClause = List.filled(eventIds.length, '?').join(',');

    await db.delete(
      _tableName,
      where: 'id IN ($inClause)',
      whereArgs: eventIds,
    );
  }

  /// Increments retry count on transmission failure.
  Future<void> recordFailure(List<String> eventIds) async {
    if (eventIds.isEmpty) return;
    if (kIsWeb) return;

    final Database db = await database;
    final String inClause = List.filled(eventIds.length, '?').join(',');

    await db.rawUpdate(
      'UPDATE $_tableName SET retry_count = retry_count + 1 WHERE id IN ($inClause)',
      eventIds,
    );
  }

  /// Gets the count of pending telemetry events.
  Future<int> countPending() async {
    if (kIsWeb) return _webInMemoryQueue.length;

    final Database db = await database;
    final List<Map<String, dynamic>> result = await db.rawQuery(
      'SELECT COUNT(*) as count FROM $_tableName WHERE submitted = 0',
    );
    return Sqflite.firstIntValue(result) ?? 0;
  }

  /// Discards stale events older than 7 days or beyond max limit.
  Future<void> _enforceCapacity() async {
    if (kIsWeb) return;

    final Database db = await database;
    final int count = await countPending();
    if (count > SecurityConstants.maxOfflineEvents) {
      final int excess = count - SecurityConstants.maxOfflineEvents;
      await db.execute('''
        DELETE FROM $_tableName WHERE id IN (
          SELECT id FROM $_tableName WHERE submitted = 0 ORDER BY created_at ASC LIMIT $excess
        )
      ''');
    }
  }

  /// Clears queue.
  Future<void> clearQueue() async {
    if (kIsWeb) {
      _webInMemoryQueue.clear();
      return;
    }

    final Database db = await database;
    await db.delete(_tableName);
  }
}
