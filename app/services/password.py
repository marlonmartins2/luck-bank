from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Password():
    @staticmethod
    def get_password_hash(password):
        """
        Get password hash
        Args:
            password (str): Password
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
        Verify password
        Args:
            plain_password (str): Plain password
            hashed_password (str): Hashed password
        """
        return pwd_context.verify(plain_password, hashed_password)
