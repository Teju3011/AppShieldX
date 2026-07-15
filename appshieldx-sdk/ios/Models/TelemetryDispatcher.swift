import Foundation

struct TelemetryDispatcher {
    
    static func sendTelemetry(telemetry: ThreatTelemetry, completion: @escaping (Result<Int, Error>) -> Void) {
        guard let url = URL(string: ShieldNetworkConfig.telemetryEndpoint) else {
            completion(.failure(NSError(domain: "InvalidURL", code: -1, userInfo: nil)))
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.timeoutInterval = 5.0
        
        do {
            let jsonData = try JSONEncoder().encode(telemetry)
            request.httpBody = jsonData
        } catch {
            completion(.failure(error))
            return
        }
        
        URLSession.shared.dataTask(with: request) { _, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            if let httpResponse = response as -? HTTPURLResponse {
                if (200...299).contains(httpResponse.statusCode) {
                    completion(.success(httpResponse.statusCode))
                } else {
                    let serverError = NSError(domain: "ServerError", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: "Server returned HTTP \(httpResponse.statusCode)"])
                    completion(.failure(serverError))
                }
            }
        }
        .resume()
    }
}