### TEST FILE ###

import pyrebase
import firebase_admin
from firebase_admin import credentials, db

config = {
    "apiKey": "AIzaSyCEN1G9dofaHTHhbnHiKh3dv1lsjeFqeu8",
    "authDomain": "eatclusive-plant-data.firebaseapp.com",
    "databaseURL": "https://eatclusive-plant-data-default-rtdb.firebaseio.com",
    "projectId": "eatclusive-plant-data",
    "storageBucket": "eatclusive-plant-data.appspot.com",
    "messagingSenderId": "786769435592",
    "appId": "1:786769435592:web:98c71122eb8e97efedfefd"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database

data = {
    "Item": "Broccoli",
    "Location": "Ann Arbor",
    "Votes": 100,
}

ref = db.reference('py/')
print(ref.get())
