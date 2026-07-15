import Foundation

struct User: Identifiable {
    let id: String
    let username: String
    let email: String
    var isActive: Bool = true
}