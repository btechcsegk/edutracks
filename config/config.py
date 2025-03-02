from pymongo.mongo_client import MongoClient
uri ="mongodb+srv://govind8061:gk806161@changetrace.hgnnz.mongodb.net/?retryWrites=true&w=majority&appName=changetrace"
# Create a new client and connect to the server
client = MongoClient(uri)

db = client['office']
usersCollection = db['users']