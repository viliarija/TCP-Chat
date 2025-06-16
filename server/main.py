import database 

db = database.db()

UID = db.getUID("admin@example.com")
connections = db.getConnections(UID)

print(UID, connections)

