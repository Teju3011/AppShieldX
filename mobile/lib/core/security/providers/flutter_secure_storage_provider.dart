import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../../error/exceptions.dart';
import 'secure_storage_provider.dart';

/// Concrete implementation of [SecureStorageProvider] backed by Android Keystore and iOS Keychain.
class FlutterSecureStorageProvider implements SecureStorageProvider {
  final FlutterSecureStorage _storage;
  final Map<String, String> _webMemoryFallback = {};

  FlutterSecureStorageProvider({FlutterSecureStorage? storage})
      : _storage = storage ??
            const FlutterSecureStorage(
              aOptions: AndroidOptions(
                encryptedSharedPreferences: true,
                keyCipherAlgorithm:
                    KeyCipherAlgorithm.RSA_ECB_OAEPwithSHA_256andMGF1Padding,
                storageCipherAlgorithm: StorageCipherAlgorithm.AES_GCM_NoPadding,
              ),
              iOptions: IOSOptions(
                accessibility: KeychainAccessibility.first_unlock_this_device,
                synchronizable: false,
              ),
            );

  @override
  Future<void> write(String key, String value) async {
    if (kIsWeb) {
      _webMemoryFallback[key] = value;
      return;
    }
    try {
      await _storage.write(key: key, value: value);
    } catch (e) {
      _webMemoryFallback[key] = value;
    }
  }

  @override
  Future<String?> read(String key) async {
    if (kIsWeb) {
      return _webMemoryFallback[key];
    }
    try {
      return await _storage.read(key: key) ?? _webMemoryFallback[key];
    } catch (e) {
      return _webMemoryFallback[key];
    }
  }

  @override
  Future<void> delete(String key) async {
    if (kIsWeb) {
      _webMemoryFallback.remove(key);
      return;
    }
    try {
      await _storage.delete(key: key);
      _webMemoryFallback.remove(key);
    } catch (e) {
      _webMemoryFallback.remove(key);
    }
  }

  @override
  Future<bool> containsKey(String key) async {
    if (kIsWeb) {
      return _webMemoryFallback.containsKey(key);
    }
    try {
      return await _storage.containsKey(key: key) || _webMemoryFallback.containsKey(key);
    } catch (e) {
      return _webMemoryFallback.containsKey(key);
    }
  }

  @override
  Future<void> clearAll() async {
    _webMemoryFallback.clear();
    if (!kIsWeb) {
      try {
        await _storage.deleteAll();
      } catch (_) {}
    }
  }
}
