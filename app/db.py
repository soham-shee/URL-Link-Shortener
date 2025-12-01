from pymongo import MongoClient
from app.config import settings
import certifi

mongo = MongoClient(
    settings.MONGO_URL,
    tls=True,
    tlsCAFile=certifi.where()
)

db = mongo["urlshort"]
urls=db["url"]
