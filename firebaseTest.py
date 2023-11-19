import firebase_admin
import threading
from time import sleep
from firebase_admin import credentials
from firebase_admin import firestore

# Fetch the service account key JSON file contents
cred = credentials.Certificate('eatclusive-plant-data-firebase-adminsdk-3xb6s-cb1f31e924.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://eatclusive-plant-data-default-rtdb.firebaseio.com/'
})

db = firestore.client()
# example of how to read data
# result = db.collection('people').document("person1").get()
# if result.exists:
#     print(result.to_dict())
    

# Create an Event for notifying main thread.
callback_done = threading.Event()

# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(f"Received document snapshot: {doc.id}")
    callback_done.set()

doc_ref = db.collection("users")

# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)
while True:
    sleep(1)
    print("Waiting for callback...")
    callback_done.wait()
    print("Callback received!")
    docs = db.collection('users').get()
    for doc in docs:
        print(doc.to_dict())
    callback_done.clear()