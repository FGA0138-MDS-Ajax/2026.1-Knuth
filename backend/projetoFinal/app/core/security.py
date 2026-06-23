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
        username = payload.get("sub")
        if not isinstance(username, str) or username == "":
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
    
def possui_permissao(permissoes: list[str] | str):
    if isinstance(permissoes, str):
        permissoes = [permissoes]

    def _dependency(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username = payload.get("sub")
            if not isinstance(username, str) or username == "":
                raise credentials_exception

            role_checks = {
                "PROFESSOR": payload.get("is_professor", False),
                "ALUNO": payload.get("is_aluno", False),
                "ADMIN": payload.get("is_admin", False),
                "QUALQUER": True
            }

            if not any(role_checks.get(perm, False) for perm in permissoes):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão necessária")
            return username
        except JWTError:
            raise credentials_exception

    return _dependency
    
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

