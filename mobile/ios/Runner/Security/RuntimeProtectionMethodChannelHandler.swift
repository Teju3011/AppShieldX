import Foundation
import Flutter

/// MethodChannel bridge dispatching Flutter RASP requests to native Swift detectors.
public class RuntimeProtectionMethodChannelHandler: NSObject {

    public static let channelName = "com.framework.security/runtime_protection"

    private let jailbreakDetector = JailbreakDetector()
    private let simulatorDetector = SimulatorDetector()
    private let debuggerDetector = DebuggerDetector()
    private let fridaDetector = FridaDetector()
    private let integrityChecker = IntegrityChecker()

    public static func register(with registrar: FlutterPluginRegistrar) {
        let channel = FlutterMethodChannel(name: channelName, binaryMessenger: registrar.messenger())
        let instance = RuntimeProtectionMethodChannelHandler()
        registrar.addMethodCallDelegate(instance, channel: channel)
    }

    public func handle(_ call: FlutterMethodCall, result: @escaping FlutterResult) {
        switch call.method {
        case "checkRootOrJailbreak":
            result(jailbreakDetector.isJailbroken())

        case "checkEmulatorOrSimulator":
            result(simulatorDetector.isSimulator())

        case "checkDebuggerAttached":
            result(debuggerDetector.isDebuggerAttached())

        case "checkFrida":
            result(fridaDetector.isFridaPresent())

        case "verifyIntegrity":
            let args = call.arguments as? [String: Any]
            let expectedSignature = args?["expectedSignature"] as? String
            result(integrityChecker.verifyIntegrity(expectedExecutableSha256: expectedSignature))

        case "getComprehensiveStatus":
            let isJailbroken = jailbreakDetector.isJailbroken()
            let isSimulator = simulatorDetector.isSimulator()
            let isDebugger = debuggerDetector.isDebuggerAttached()
            let isFrida = fridaDetector.isFridaPresent()
            let isIntegrityValid = integrityChecker.verifyIntegrity(expectedExecutableSha256: nil)

            var threats: [String] = []
            if isJailbroken { threats.append("JAILBREAK_DETECTED") }
            if isSimulator { threats.append("SIMULATOR_DETECTED") }
            if isDebugger { threats.append("DEBUGGER_DETECTED") }
            if isFrida { threats.append("FRIDA_DETECTED") }
            if !isIntegrityValid { threats.append("INTEGRITY_FAILURE") }

            let statusMap: [String: Any] = [
                "rootDetected": false,
                "jailbreakDetected": isJailbroken,
                "emulatorDetected": false,
                "simulatorDetected": isSimulator,
                "debuggerDetected": isDebugger,
                "fridaDetected": isFrida,
                "integrityValid": isIntegrityValid,
                "sslPinningEnabled": true,
                "secureStorageAvailable": true,
                "detectedThreats": threats,
                "platform": "ios",
                "timestamp": ISO8601DateFormatter().string(from: Date())
            ]

            result(statusMap)

        default:
            result(FlutterMethodNotImplemented)
        }
    }
}
