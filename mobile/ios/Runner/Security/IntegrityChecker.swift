import Foundation
import CommonCrypto

/// Native iOS Application Binary & Bundle Integrity Checker.
public class IntegrityChecker {

    private static let expectedBundleIdentifier = "com.framework.security"

    public init() {}

    /// Verifies application bundle identifier and main executable binary integrity.
    public func verifyIntegrity(expectedExecutableSha256: String?) -> Bool {
        guard checkBundleIdentifier() else {
            return false
        }

        if let expectedHash = expectedExecutableSha256, !expectedHash.isEmpty {
            guard let currentHash = getExecutableSha256() else { return false }
            return currentHash.uppercased() == expectedHash.replacingOccurrences(of: ":", with: "").uppercased()
        }

        return true
    }

    /// Probe 1: Ensures the runtime bundle identifier has not been altered during repackaging.
    public func checkBundleIdentifier() -> Bool {
        guard let currentId = Bundle.main.bundleIdentifier else { return false }
        return currentId == Self.expectedBundleIdentifier || currentId.hasPrefix("com.framework.security")
    }

    /// Probe 2: Computes SHA-256 checksum of the main Mach-O executable file.
    public func getExecutableSha256() -> String? {
        guard let executablePath = Bundle.main.executablePath else { return nil }
        guard let fileData = FileManager.default.contents(atPath: executablePath) else { return nil }

        var digest = [UInt8](repeating: 0, count: Int(CC_SHA256_DIGEST_LENGTH))
        fileData.withUnsafeBytes {
            _ = CC_SHA256($0.baseAddress, CC_LONG(fileData.count), &digest)
        }

        return digest.map { String(format: "%02X", $0) }.joined()
    }
}
