### TEST FILE ###

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('eatclusive-plant-data-firebase-adminsdk-3xb6s-cb1f31e924.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://eatclusive-plant-data-default-rtdb.firebaseio.com'
})

ref = db.reference('py/')
users_ref = ref.child('items')
users_ref.set({
    'Broccoli': {
        'Location': 'Ann Arbor'
    }
})

hopper_ref = users_ref.child('Broccoli')

handle = db.reference('py/items/broccoli')

print(ref.get())
