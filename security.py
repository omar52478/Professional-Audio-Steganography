# security.py
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64

def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a cryptographic key from a password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_data(data: bytes, password: str) -> bytes:
    """Encrypts data with a password."""
    if not password:
        return data
    salt = os.urandom(16)
    key = derive_key(password, salt)
    f = Fernet(key)
    encrypted_data = f.encrypt(data)
    return salt + encrypted_data # Prepend salt to the encrypted data

def decrypt_data(encrypted_data_with_salt: bytes, password: str) -> bytes:
    """Decrypts data with a password."""
    if not password:
        return encrypted_data_with_salt
    try:
        salt = encrypted_data_with_salt[:16]
        encrypted_data = encrypted_data_with_salt[16:]
        key = derive_key(password, salt)
        f = Fernet(key)
        return f.decrypt(encrypted_data)
    except Exception as e:
        raise ValueError(f"Decryption failed. Incorrect password or corrupted data. Details: {e}")