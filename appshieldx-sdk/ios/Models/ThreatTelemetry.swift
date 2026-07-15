import Foundation

struct ThreatTelemetry: Codable {
    let deviceId: String
    let osVersion: String
    let isRooted: Bool
    let isEmulator: Bool
    let integrityStatus: String
    let timestamp: Int64
    
    init(deviceId: String, osVersion: String, isRooted: Bool, isEmulator: Bool, integrityStatus: String) {
        self.deviceId = deviceId
        self.osVersion = osVersion
        self.isRooted = isRooted
        self.isEmulator = isEmulator
        self.integrityStatus = integrityStatus
        self.timestamp = Int64(Date().timeIntervalSince1970 * 1000)
    }
}