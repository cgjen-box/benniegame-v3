import SwiftUI
import Lottie

struct ContentView: View {
    var body: some View {
        VStack {
            Image(systemName: "bear.fill")
                .imageScale(.large)
                .foregroundStyle(.brown)
            Text("Bennie und die Lemminge")
                .font(.largeTitle)
        }
        .padding()
    }
}

#Preview {
    ContentView()
}
