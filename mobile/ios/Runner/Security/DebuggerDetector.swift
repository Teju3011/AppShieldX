import Foundation
import Darwin

/// Native iOS Debugger & Tracer Detection Engine.
///
/// Queries low-level Mach/BSD process control flags (sysctl P_TRACED)
/// to identify active LLDB attachments or interactive process tracing.
public class DebuggerDetector {

    public init() {}

    /// Checks whether an active debugger or tracer is attached to the current process.
    public func isDebuggerAttached() -> Bool {
        return checkSysctlPTraced()
    }

    /// Probe 1: Queries BSD process structure via sysctl for the P_TRACED bit flag.
    public func checkSysctlPTraced() -> Bool {
        var mib = [CTL_KERN, KERN_PROC, KERN_PROC_PID, getpid()]
        var info = kinfo_proc()
        var size = MemoryLayout<kinfo_proc>.stride

        let result = sysctl(&mib, u_int(mib.count), &info, &size, nil, 0)
        guard result == 0 else {
            return false
        }

        // p_flag bitwise AND with P_TRACED indicates debugger is attached
        return (info.kp_proc.p_flag & P_TRACED) != 0
    }

    /// Denies future debugger attachment via ptrace PT_DENY_ATTACH.
    /// Note: Calling this terminates the process if a debugger is already connected.
    public func denyDebuggerAttach() {
        #if !DEBUG
        // Dynamic symbol resolution to invoke ptrace(PT_DENY_ATTACH, 0, 0, 0)
        let handle = dlopen(nil, RTLD_GLOBAL | RTLD_NOW)
        if let handle = handle {
            typealias PtraceType = @convention(c) (CInt, pid_t, CInt, CInt) -> CInt
            let sym = dlsym(handle, "ptrace")
            if let sym = sym {
                let ptrace = unsafeBitCast(sym, to: PtraceType.self)
                let PT_DENY_ATTACH: CInt = 31
                _ = ptrace(PT_DENY_ATTACH, 0, 0, 0)
            }
            dlclose(handle)
        }
        #endif
    }
}
