from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime 

app = Flask(__name__)


MONGO_URI = "mongodb+srv://Hayin:Helion2949@secretiveplotter.5xgc1.mongodb.net/?retryWrites=true&w=majority&appName=Secretiveplotter"
client = MongoClient(MONGO_URI)
db = client["sensor_db"]  
collection = db["sensor_data"] 

@app.route('/sensor', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()  # Ambil data dari ESP32
        data["timestamp"] = datetime.datetime.now()  # Tambahkan timestamp
        collection.insert_one(data)  # Simpan ke MongoDB
        return jsonify({"status": "success", "message": "Data berhasil disimpan!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


@app.route('/get_data', methods=['GET'])
def get_data():
    latest_data = collection.find().sort("_id", -1).limit(1)  # Ambil data terbaru
    data = list(latest_data)
    
    if data:
        response = {
            "temperature": data[0]["temperature"],
            "humidity": data[0]["humidity"]
        }
        return jsonify(response), 200
    else:
        return jsonify({"message": "No data found"}), 404