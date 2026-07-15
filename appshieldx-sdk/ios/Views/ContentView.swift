import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = MainViewModel()

    var body: some View {
        VStack(spacing: 16) {
            if let user = viewModel.userState {
                VStack(alignment: .leading, spacing: 8) {
                    Text("Model Loaded Successfully!")
                        .font(.headline)
                    Text("ID: \(user.id)")
                    Text("User: \(user.username)")
                    Text("Email: \(user.email)")
                }
                .padding()
                .background(Color(.secondarySystemBackground))
                .cornerRadius(12)
            } else {
                Text("iOS Core Framework: Ready")
                    .font(.title2)

                Button(action: {
                    viewModel.initializeFrameworkUser()
                }) {
                    Text("Load Framework Model")
                        .bold()
                        .foregroundColor(.white)
                        .padding()
                        .background(Color.blue)
                        .cornerRadius(8)
                }
            }
        }
        .padding()
    }
}