from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.utils.settings import settings
from jwt.exceptions import InvalidTokenError
import jwt
from src.user.models import UserModel
from src.utils.db import get_db

### ! Token send

def is_authenticate(request:Request, db:Session = Depends(get_db)):
    try:
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized.")
        toten = token.split(" ")[-1]
        
        data = jwt.decode(toten, settings.SECRETE_KEY, settings.ALGORITHM)
        user_id = data.get("_id")
        
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized.")

        return user
    except InvalidTokenError:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized.")