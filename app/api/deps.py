from fastapi import Header, HTTPException
from app.database import SessionLocal
from app.models import User

def endpoints(api_key: str = Header(..., alias="api-key")):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.name == api_key).first()
        if user is None:
            raise HTTPException(
        status_code=401,
        detail={
            "result": False,
            "error_type": "unauthorized",
            "error_message": "Invalid api-key",
        }, )
        return user
    finally:
        db.close()



