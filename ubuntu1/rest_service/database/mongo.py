from pymongo import MongoClient
import os

# Se o Flask estiver fora do Docker, usa "localhost"
# Se estiver em container Docker, usa "projeto_mongodb"
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

db = client["esteroides_db"]
collection = db["esteroides"]
users_collection = db["users"]
