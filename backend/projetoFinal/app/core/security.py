from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_current_username(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

def get_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception

def get_current_professor(payload: dict = Depends(get_token_payload)):
    if not payload.get("is_professor"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário não possui permissão de professor"
        )
    return payload.get("sub")

def get_current_monitor(payload: dict = Depends(get_token_payload)):
    if not payload.get("is_monitor"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário não possui permissão de monitor"
        )
    return payload.get("sub")

def get_current_admin(payload: dict = Depends(get_token_payload)):
    if not payload.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário não possui permissão de administrador"
        )
    return payload.get("sub")

def get_current_staff(payload: dict = Depends(get_token_payload)):
    if not (payload.get("is_professor") or payload.get("is_monitor")):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário não possui permissão de professor ou monitor"
        )
    return payload.get("sub")
    
def verify_password(plain_password, hashed_password):
    #return True
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None 

#from fastapi.security import HTTPBasic, HTTPBasicCredentials
#from app.core.config import settings
#import secrets

#security = HTTPBasic()

#def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
#    correct_username = secrets.compare_digest(credentials.username, settings.BASIC_AUTH_USERNAME)
#    correct_password = secrets.compare_digest(credentials.password, settings.BASIC_AUTH_PASSWORD)
#    if not (correct_username and correct_password):
#        raise HTTPException(
#            status_code=status.HTTP_401_UNAUTHORIZED,
#            detail="Incorrect username or password",
#            headers={"WWW-Authenticate": "Basic"},
#        )
#    return credentials.username