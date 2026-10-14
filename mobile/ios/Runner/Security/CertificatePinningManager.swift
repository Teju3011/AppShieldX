import Foundation
import Security
import CommonCrypto

/// Native iOS Certificate & Public Key Pinning Manager.
public class CertificatePinningManager {

    private let pinnedHashes: [String]

    public init(pinnedHashes: [String]) {
        self.pinnedHashes = pinnedHashes
    }

    /// Verifies that a server certificate's public key matches pinned SHA-256 SPKI hashes.
    public func verifyServerTrust(serverTrust: SecTrust, domain: String?) -> Bool {
        guard !pinnedHashes.isEmpty else { return true }

        let certCount = SecTrustGetCertificateCount(serverTrust)
        guard certCount > 0 else { return false }

        for i in 0..<certCount {
            if let cert = SecTrustGetCertificateAtIndex(serverTrust, i) {
                if let publicKey = SecCertificateCopyKey(cert) {
                    if let spkiHash = getPublicKeySha256(publicKey: publicKey) {
                        for pinned in pinnedHashes {
                            let cleanPin = pinned.replacingOccurrences(of: "sha256/", with: "")
                                                 .replacingOccurrences(of: ":", with: "")
                                                 .uppercased()
                            if cleanPin == spkiHash.uppercased() {
                                return true // Pin matched
                            }
                        }
                    }
                }
            }
        }

        return false // Pin mismatch
    }

    private func getPublicKeySha256(publicKey: SecKey) -> String? {
        var error: Unmanaged<CFError>?
        guard let keyData = SecKeyCopyExternalRepresentation(publicKey, &error) as Data? else {
            return nil
        }

        var digest = [UInt8](repeating: 0, count: Int(CC_SHA256_DIGEST_LENGTH))
        keyData.withUnsafeBytes {
            _ = CC_SHA256($0.baseAddress, CC_LONG(keyData.count), &digest)
        }

        return digest.map { String(format: "%02X", $0) }.joined()
    }
}
