
from firebase_admin import credentials
from firebase_admin import db
import firebase_admin

cred = credentials.Certificate('fetch/cred.json')
url = 'https://neosalpha-999-default-rtdb.firebaseio.com/'
path = {'databaseURL' : url}

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, path)

def call(path = 'taxiwars'):
    refv = db.reference(path)
    name = refv.get()
    return name

def send(path, data = {}):
    refv = db.reference(path)
    refv.set(data)
