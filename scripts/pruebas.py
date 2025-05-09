from pymongo import MongoClient

uri = "mongodb://0.tcp.ngrok.io:17736/?replicaSet=rs0"


try:
    cliente = MongoClient(uri, serverSelectionTimeoutMS=5000)  # 5s timeout
    cliente.server_info()  # Forzar intento de conexión
    print("✅ Conexión exitosa a MongoDB remotamente.")
except Exception as e:
    print("❌ Error de conexión:", e)
