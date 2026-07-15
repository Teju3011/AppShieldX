import Foundation

struct ShieldNetworkConfig {
    // Localhost routes perfectly from native iOS targets straight to your machine's gateway port
    private static let gatewayHost = "http://localhost:8080"
    
    static var telemetryEndpoint: String {
        return "\(gatewayHost)/v1/telemetry"
    }
    
    static var checkStatusEndpoint: String {
        return "\(gatewayHost)/v1/status"
    }
}