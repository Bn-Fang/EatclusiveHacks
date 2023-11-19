### TEST FILE ###
# Most of the things work in ehre #

import os
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore


# setup
cred = credentials.Certificate("eatclusive-plant-data-firebase-adminsdk-3xb6s-cb1f31e924.json")
firebase_admin.initialize_app(cred)

# "https://raw.githubusercontent.com/Bn-Fang/EatclusiveHacks/main/VotingData.csv"
#df = pd.read_csv(folder_path)

db = firestore.client()

collection_ref = db.collection('people')

def on_snapshot(col_snapshot, changes, real_time):
    print(f'Callback received query snapshot.')
    print(f'Current cities in California: ')
    for doc in col_snapshot:
        print(f'{doc.id}')

col_watch = collection_ref.on_snapshot(on_snapshot)

#docs = collection_ref.stream()

#for doc in docs:
#    doc_ref = collection_ref.document(doc.id)
#    update_data = {
#        'vote': 0,
#    }

#   doc_ref.update(update_data)

#result = db.collection('users').document(str(1371)).get()
#user_db = db.collection('users').document(str(1371))

#if result.exists:
#    user_data = {
#        'vote': 0,
#    }

#user_db.update(user_data)
