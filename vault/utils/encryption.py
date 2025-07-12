from cryptography.fernet import Fernet
from django.conf import settings

# Generate a key ONCE and store securely (not regenerate every time)
key = settings.SECRET_KEY[:32].encode()  # use a portion of SECRET_KEY
fernet = Fernet(Fernet.generate_key())  # replace with a stable key

def encrypt_password(password: str) -> str:
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password: str) -> str:
    return fernet.decrypt(encrypted_password.encode()).decode()
