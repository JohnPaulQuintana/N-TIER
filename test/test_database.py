from database.connection import SessionLocal


db = SessionLocal()

print("Session created:", db)

db.close()

print("Session closed")