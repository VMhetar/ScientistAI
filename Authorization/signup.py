from fastapi import APIRouter, HTTPException
from auth_utils import hash_password

router = APIRouter()

fake_db = {} 


@router.post("/signup")
async def signup(email: str, password: str):
    if email in fake_db:
        raise HTTPException(status_code=400, detail="User already exists")

    password_hash = hash_password(password)

    fake_db[email] = {
        "email": email,
        "password_hash": password_hash
    }

    return {"message": "User created"}
