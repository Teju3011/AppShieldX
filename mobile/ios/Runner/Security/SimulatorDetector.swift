import Foundation

/// Native iOS Simulator & Virtualized Environment Detection Engine.
public class SimulatorDetector {

    public init() {}

    /// Evaluates compile-time environment flags and runtime Darwin environment variables.
    public func isSimulator() -> Bool {
        #if targetEnvironment(simulator)
        return true
        #else
        return checkRuntimeEnvironmentVariables() || checkDarwinHardwareModel()
        #endif
    }

    /// Probe 1: Inspects ProcessInfo environment variables injected by Xcode CoreSimulator.
    public func checkRuntimeEnvironmentVariables() -> Bool {
        let env = ProcessInfo.processInfo.environment
        return env["SIMULATOR_DEVICE_NAME"] != nil ||
               env["SIMULATOR_MODEL_IDENTIFIER"] != nil ||
               env["SIMULATOR_ROOT"] != nil
    }

    /// Probe 2: Queries hw.machine sysctl property for simulator architecture flags.
    public func checkDarwinHardwareModel() -> Bool {
        var size = 0
        sysctlbyname("hw.machine", nil, &size, nil, 0)
        var machine = [CChar](repeating: 0, count: size)
        sysctlbyname("hw.machine", &machine, &size, nil, 0)
        let model = String(cString: machine).lowercased()

        return model.contains("x86_64") || model.contains("i386")
    }
}
