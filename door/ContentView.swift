/// (c) Justus Languell <jus@justusl.com>

import SwiftUI
import FirebaseCore
import FirebaseFirestore

struct ContentView: View {
    var body: some View {
        VStack {
            
            // App buisness logic
        
            Button {
                handleOpen()
            }
                label: {
                    Text("Open 😎").frame(maxWidth: .infinity, maxHeight: 300)
                }
            .buttonStyle(.borderedProminent)
            
        } .padding()
    }
}

var db: Firestore? = nil;


func handleOpen() {
    let t = Int64(NSDate().timeIntervalSince1970)
        
    if (db == nil) {
        FirebaseApp.configure()
        db = Firestore.firestore()
    }
    
    db?.collection("req").document("req")
        .updateData([
          "req": FieldValue.arrayUnion([t])
        ])
      
}

#Preview {
    ContentView()
}
