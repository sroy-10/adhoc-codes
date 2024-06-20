# pip install cryptography  

###########################################################################
# ENCRYPTION DATA
###########################################################################
from base64 import b64encode
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def derive_key(password, salt):
    N = 16384
    r = 8
    p = 1
    dk_len = 32  # Desired key length in bytes

    kdf = Scrypt(salt=salt, length=dk_len, n=N, r=r, p=p, backend=default_backend())
    key = kdf.derive(password)
    return key

def encrypt_data(data, password, salt):
    try:
        # Derive the key
        password_bytes = password.encode()
        salt_bytes = salt.encode()
        key = derive_key(password_bytes, salt_bytes)

        # Generate a random IV
        iv = os.urandom(12)  # 12 bytes for AES-GCM IV

        # Encrypt the data
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data.encode()) + encryptor.finalize()

        # Combine IV, ciphertext, and tag
        encrypted_data = iv + ciphertext + encryptor.tag

        # Encode the combined data to base64
        encrypted_data_base64 = b64encode(encrypted_data).decode("utf-8")
        return encrypted_data_base64
    except Exception as e:
        print(f"Encryption failed: {e}")
        return None

# Example usage
data = "subhajit.e.roy"
password = "MIIBIjANBgkqhkiG9"
salt = "lkgmpotomtm"

encrypted_data = encrypt_data(data, password, salt)
print("Encrypted data:", encrypted_data)

###########################################################################
# DECRYPTION DATA
###########################################################################
from base64 import b64decode
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


def derive_key(password, salt):
    N = 16384
    r = 8
    p = 1
    dk_len = 32  # Desired key length in bytes

    kdf = Scrypt(salt=salt, length=dk_len, n=N, r=r, p=p, backend=default_backend())
    key = kdf.derive(password)
    return key

def decrypt_data(encrypted_data, password, salt):
    try:
        encrypted_data_bytes = b64decode(encrypted_data)

        # Extract the IV, the actual encrypted data, and the authentication tag
        iv = encrypted_data_bytes[:12]
        ciphertext_and_tag = encrypted_data_bytes[12:]
        ciphertext = ciphertext_and_tag[:-16]
        tag = ciphertext_and_tag[-16:]

        # Derive the key
        password_bytes = password.encode()
        salt_bytes = salt.encode()
        key = derive_key(password_bytes, salt_bytes)

        # Decrypt the data
        cipher = Cipher(
            algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend()
        )
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

        # Convert decrypted data to string
        decrypted_data = decrypted_data.decode("utf-8")
        return decrypted_data
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

# Example usage
encrypted_data_js = (
    "KXqSVJlB+WPv4JUPpsbCKJJWWmfhGFLre7UYFvcoXvJdZru3ROQK7HYGWGxWRlMhtCSIGSFWBFs="
)
password = "MIIBIjANBgkqhkiG9"
salt = "lkgmpotomtm"

decrypted_data = decrypt_data(encrypted_data_js, password, salt)
print("Decrypted data:", decrypted_data)
