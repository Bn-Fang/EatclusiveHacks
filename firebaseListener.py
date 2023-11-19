import firebase_admin
import threading
from time import sleep
from firebase_admin import credentials
from firebase_admin import firestore
import os

# Fetch the service account key JSON file contents
cred = credentials.Certificate('eatclusive-plant-data-firebase-adminsdk-3xb6s-cb1f31e924.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://eatclusive-plant-data-default-rtdb.firebaseio.com/'
})

db = firestore.client()

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
    os.system("/usr/local/bin/python3 /Users/benfang/Documents/Mhacks16/EatclusiveHacks/ClusterLocator.py")
    callback_done.clear()