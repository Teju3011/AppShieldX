import 'package:uuid/uuid.dart';
import '../constants/security_constants.dart';
import '../security/providers/secure_storage_provider.dart';

/// Utilities for generating and persistently retrieving hardware/device-level unique fingerprints.
class DeviceFingerprint {
  final SecureStorageProvider _storage;

  DeviceFingerprint(this._storage);

  /// Retrieves the existing device ID from secure storage, or creates and stores a new UUIDv4.
  Future<String> getDeviceId() async {
    final String? existing =
        await _storage.read(SecurityConstants.storageDeviceIdKey);
    if (existing != null && existing.isNotEmpty) {
      return existing;
    }

    final String newId = const Uuid().v4();
    await _storage.write(SecurityConstants.storageDeviceIdKey, newId);
    return newId;
  }
}
