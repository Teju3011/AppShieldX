/// Certificate and public-key pinning configuration for network layer TLS verification.
class PinningConfig {
  final String hostname;
  final List<String> spkiHashesSHA256;
  final bool enforcePinning;

  const PinningConfig({
    required this.hostname,
    required this.spkiHashesSHA256,
    this.enforcePinning = true,
  });

  /// Validates whether a provided SHA-256 fingerprint matches any pinned hash.
  bool isValidFingerprint(String fingerprint) {
    if (!enforcePinning) return true;
    final normalized = fingerprint.replaceAll(':', '').toUpperCase();
    return spkiHashesSHA256.any((hash) {
      final cleanHash = hash
          .replaceAll('sha256/', '')
          .replaceAll(':', '')
          .toUpperCase();
      return normalized == cleanHash;
    });
  }
}
