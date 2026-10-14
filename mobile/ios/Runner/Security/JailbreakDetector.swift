import Foundation
import UIKit
import Darwin

/// Native iOS Jailbreak & Sandbox Integrity Detection Engine.
///
/// Implements multi-layered probes checking jailbreak filesystem artifacts,
/// sandbox escape capabilities, system call fork availability, and injected dynamic libraries.
public class JailbreakDetector {

    private static let jailbreakPaths = [
        "/Applications/Cydia.app",
        "/Library/MobileSubstrate/MobileSubstrate.dylib",
        "/bin/bash",
        "/usr/sbin/sshd",
        "/etc/apt",
        "/usr/bin/ssh",
        "/private/var/lib/apt",
        "/private/var/lib/cydia",
        "/Applications/Sileo.app",
        "/Applications/Zebra.app",
        "/var/binpack",
        "/Library/PreferenceBundles/LibertyPref.bundle",
        "/Library/PreferenceBundles/ShadowPreferences.bundle"
    ]

    private static let suspiciousDylibs = [
        "MobileSubstrate",
        "CydiaSubstrate",
        "SubstrateLoader",
        "SubstrateInserter",
        "libhooker",
        "substitute"
    ]

    public init() {}

    /// Executes all jailbreak detection heuristics and returns true if any probe triggers.
    public func isJailbroken() -> Bool {
        #if targetEnvironment(simulator)
        return false // Bypass on simulator to prevent false positives from host Darwin filesystem
        #else
        return checkFilesystemPaths() ||
               checkSandboxEscape() ||
               checkForkSyscall() ||
               checkDyldInjectedLibraries()
        #endif
    }

    /// Probe 1: Checks for existence of standard jailbreak files and package managers.
    public func checkFilesystemPaths() -> Bool {
        let fileManager = FileManager.default
        for path in Self.jailbreakPaths {
            if fileManager.fileExists(atPath: path) {
                return true
            }
        }
        return false
    }

    /// Probe 2: Attempts to write a test payload outside of the sandboxed container.
    public func checkSandboxEscape() -> Bool {
        let testPath = "/private/jailbreak_sandbox_test.txt"
        let testString = "JailbreakSandboxVerificationTest"
        do {
            try testString.write(toFile: testPath, atomically: true, encoding: .utf8)
            try? FileManager.default.removeItem(atPath: testPath)
            return true // Successfully writing outside sandbox indicates root access
        } catch {
            return false // Write failed as expected in a secure sandbox
        }
    }

    /// Probe 3: Calls fork(). In standard iOS sandbox, fork() returns -1 with errno EPERM.
    public func checkForkSyscall() -> Bool {
        let pid = fork()
        if pid >= 0 {
            if pid > 0 {
                var status: Int32 = 0
                waitpid(pid, &status, 0)
            } else {
                exit(0)
            }
            return true // fork succeeded, indicating sandbox bypass
        }
        return false
    }

    /// Probe 4: Scans Mach-O dynamic linker loaded images for known hooking frameworks.
    public func checkDyldInjectedLibraries() -> Bool {
        let count = _dyld_image_count()
        for i in 0..<count {
            if let imageName = _dyld_get_image_name(i) {
                let name = String(cString: imageName).lowercased()
                for dylib in Self.suspiciousDylibs {
                    if name.contains(dylib.lowercased()) {
                        return true
                    }
                }
            }
        }
        return false
    }
}
