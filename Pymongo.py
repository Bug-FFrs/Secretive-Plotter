
from pymongo import MongoClient
import requests
import time


MONGO_URI = "mongodb+srv://Hayin:Helion2949@secretiveplotter.5xgc1.mongodb.net/?retryWrites=true&w=majority&appName=Secretiveplotter"
client = MongoClient(MONGO_URI)
db = client["sensor_db"]  
collection = db["sensor_data"]  


UBIDOTS_URL = "http://industrial.api.ubidots.com/api/v1.6/devices/dht11"
HEADERS = {
    "X-Auth-Token": "BBUS-H0shvFFL6DMPK6CzSRjnj5gapToDUV",
    "Content-Type": "application/json"
}


while True:
    latest_data = collection.find_one(sort=[("_id", -1)])  # Ambil data terbaru

    if latest_data:
        ubidots_payload = {
            "temperature": latest_data["temperature"],
            "humidity": latest_data["humidity"]
        }

        try:
            response = requests.post(UBIDOTS_URL, json=ubidots_payload, headers=HEADERS)
            print("Response dari Ubidots:", response.text)
        except Exception as e:
            print("Gagal mengirim data ke Ubidots:", e)
    else:
        print("Tidak ada data di MongoDB!")

    time.sleep(4)  # Tunggu 4 detik sebelum mengirim data lagi