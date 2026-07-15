import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = MainViewModel()

    var body: some View {
        VStack(spacing: 32) {
            Text("AppShieldX Client Toolkit")
                .font(.title)
                .bold()
            
            // Output display card wrapper
            RoundedRectangle(cornerRadius: 12)
                .fill(Color(.systemGray6))
                .frame(maxWidth: .infinity, minHeight: 200)
                .overlay(
                    Text(viewModel.securityState)
                        .font(.system(.body, design: .monospaced))
                        .padding(),
                    alignment: .topLeading
                )
            
            Button(action: {
                viewModel.runSecurityAssessment()
            }) {
                Text("Execute Core RASP Scan")
                    .font(.headline)
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .frame(height: 50)
                    .background(Color.blue)
                    .cornerRadius(10)
            }
        }
        .padding(24)
    }
}

#Preview {
    ContentView()
}