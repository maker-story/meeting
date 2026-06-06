from application.user.usecases.auth_usecase import IPasswordHasher
import bcrypt # pip install bcrypt

class BcryptPasswordHasher(IPasswordHasher):
    def hash(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')