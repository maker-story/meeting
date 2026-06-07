import jwt
import bcrypt # pip install bcrypt
from datetime import datetime, timedelta

from application.usecases.login_user_usercase import ITokenService
from application.usecases.register_user_usecase import IPasswordHasher


SECRET_KEY = "your_super_secret_key_change_me_in_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 


class BcryptPasswordHasher(IPasswordHasher):
    def hash_password(self, password: str) -> str:
        password_bytes = password.encode('utf-8')[:72]
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            password_bytes = plain_password.encode('utf-8')[:72]
            hashed_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception:
            return False


class JwtTokenService(ITokenService):
    def generate_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt