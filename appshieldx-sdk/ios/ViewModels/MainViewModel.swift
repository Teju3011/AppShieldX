import Foundation

class MainViewModel: ObservableObject {
    @Published var securityState: String = "System Initialized. Awaiting Scan..."
    
    func runSecurityAssessment() {
        DispatchQueue.main.async {
            self.securityState = "Analyzing environment status..."
        }
        
        let isJailbroken = FileManager.default.fileExists(atPath: "/Applications/Cydia.app") || 
                           FileManager.default.fileExists(atPath: "/private/var/lib/apt")
        
        #if targetEnvironment(simulator)
        let isSimulator = true
        #else
        let isSimulator = false
        #endif
        
        let telemetry = ThreatTelemetry(
            deviceId: "IOS_" + (UUID().uuidString.prefix(8)),
            osVersion: "18.0",
            isRooted: isJailbroken,
            isEmulator: isSimulator,
            integrityStatus: isJailbroken ? "COMPROMISED" : "SECURE"
        )
        
        DispatchQueue.main.async {
            self.securityState = "Transmitting metrics to secure gateway..."
        }
        
        TelemetryDispatcher.sendTelemetry(telemetry: telemetry) { result in
            DispatchQueue.main.async {
                switch result {
                case .success(let code):
                    self.securityState = """
                    Scan Transmitted! (HTTP \(code))
                    Status: \(telemetry.integrityStatus)
                    Jailbreak Detected: \(telemetry.isRooted)
                    Is Simulator: \(telemetry.isEmulator)
                    """
                case .failure(let error):
                    self.securityState = """
                    Scan Cached. Gateway Offline.
                    Reason: \(error.localizedDescription)
                    Status: \(telemetry.integrityStatus)
                    """
                }
            }
        }
    }
}