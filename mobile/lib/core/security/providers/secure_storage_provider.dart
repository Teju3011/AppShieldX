/// Abstract contract for hardware-backed encrypted key-value storage.
abstract class SecureStorageProvider {
  /// Commits a sensitive key-value pair into hardware-backed keystore.
  Future<void> write(String key, String value);

  /// Retrieves a sensitive value from hardware-backed keystore.
  Future<String?> read(String key);

  /// Removes an individual key from storage.
  Future<void> delete(String key);

  /// Queries whether a given key exists in secure storage.
  Future<bool> containsKey(String key);

  /// Purges all sensitive credentials and cached secrets from device keystore.
  Future<void> clearAll();
}
