# db.py
from pymongo import MongoClient

# Conexión a MongoDB Atlas o local
MONGO_URI = "mongodb://localhost:27017"  
client = MongoClient(MONGO_URI)

# Selección de la base de datos
db = client['avicola_llano_grande']

# Colecciones (tablas en NoSQL)
stock_collection = db['stock']
ventas_collection = db['ventas']
