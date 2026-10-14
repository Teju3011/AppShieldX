import Foundation
import Darwin
import MachO

/// Native iOS Dynamic Instrumentation & Hooking Scanner (Frida / Cycript).
///
/// Implements Mach-O dynamic image auditing, Frida export symbol scanning,
/// and local TCP port connection verification.
public class FridaDetector {

    private static let fridaPort: UInt16 = 27042
    private static let suspiciousKeywords = ["frida", "gadget", "cydiasubstrate", "cycript", "libgum"]

    public init() {}

    /// Executes all Frida dynamic hooking checks.
    public func isFridaPresent() -> Bool {
        return checkDyldImages() ||
               checkFridaSymbols() ||
               checkDefaultFridaPort()
    }

    /// Probe 1: Scans all Mach-O images loaded into current process space.
    public func checkDyldImages() -> Bool {
        let count = _dyld_image_count()
        for i in 0..<count {
            if let cName = _dyld_get_image_name(i) {
                let name = String(cString: cName).lowercased()
                for keyword in Self.suspiciousKeywords {
                    if name.contains(keyword) {
                        return true
                    }
                }
            }
        }
        return false
    }

    /// Probe 2: Attempts to resolve known exported symbols associated with Frida Gum runtime.
    public func checkFridaSymbols() -> Bool {
        let handle = dlopen(nil, RTLD_NOW)
        defer { if let handle = handle { dlclose(handle) } }

        if let handle = handle {
            if dlsym(handle, "frida_agent_main") != nil ||
               dlsym(handle, "gum_init") != nil ||
               dlsym(handle, "gum_process_enumerate_modules") != nil {
                return true
            }
        }
        return false
    }

    /// Probe 3: Connects to default Frida server socket on localhost (127.0.0.1:27042).
    public func checkDefaultFridaPort() -> Bool {
        var serverAddr = sockaddr_in()
        serverAddr.sin_family = sa_family_t(AF_INET)
        serverAddr.sin_port = Self.fridaPort.bigEndian
        serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1")

        let sock = socket(AF_INET, SOCK_STREAM, 0)
        guard sock >= 0 else { return false }
        defer { close(sock) }

        // Set non-blocking timeout
        var timeout = timeval(tv_sec: 0, tv_usec: 100000) // 100ms
        setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, socklen_t(MemoryLayout<timeval>.size))
        setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, &timeout, socklen_t(MemoryLayout<timeval>.size))

        let result = withUnsafePointer(to: &serverAddr) {
            $0.withMemoryRebound(to: sockaddr.self, capacity: 1) {
                connect(sock, $0, socklen_t(MemoryLayout<sockaddr_in>.size))
            }
        }

        return result == 0 // Connection established implies Frida server active
    }
}
