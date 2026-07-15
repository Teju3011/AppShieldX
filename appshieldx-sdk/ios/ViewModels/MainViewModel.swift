import Foundation
import Combine

class MainViewModel: ObservableObject {
    @Published var userState: User? = nil

    func initializeFrameworkUser() {
        self.userState = User(
            id = "USR-779X",
            username = "Tej30_Developer",
            email = "developer@universalapp.com"
        )
    }
}