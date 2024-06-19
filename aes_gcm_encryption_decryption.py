# !pip install pycryptodome

import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
import traceback

class AESGCMEncryptorDecryptor:
    def __init__(self, key, salt):
        self.key = key
        self.salt = salt

    def encrypt_data(self, data) -> str:
        """
        Encrypt data using AES-GCM.
        Args:
            data (str): The plaintext data to be encrypted.
        Returns:
            str: The base64 encoded encrypted data.
        """
        try:
            # Derive the AES key using scrypt
            key = scrypt(self.key, self.salt, 32, N=2**14, r=8, p=1)

            # Generate a unique nonce for this encryption
            nonce = get_random_bytes(12)

            # Initialize the AES cipher with the derived key and nonce for GCM mode
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

            # Encrypt the data
            encrypted, tag = cipher.encrypt_and_digest(data.encode("utf-8"))

            # Combine the nonce, encrypted data, and tag for transmission
            enc_data = nonce + tag + encrypted

            # Encode the combined data as base64
            return base64.b64encode(enc_data).decode("utf-8")
        except Exception as e:
            error_message = f"{e}. {traceback.format_exc()}"
            raise Exception(f"Encryption failed: {error_message}")

    def decrypt_data(self, enc) -> str:
        """
        Decrypt data using AES-GCM with the provided encrypted data.
        Args:
            enc (str): The base64 encoded encrypted data to be decrypted.
        Raises:
            Exception: If decryption fails, an exception is raised with the error message.
        Returns:
            str: The decrypted data as a UTF-8 string.
        """
        try:
            # Decode the encrypted data from base64
            enc_data = base64.b64decode(enc)

            # Derive the AES key using scrypt
            key = scrypt(self.key, self.salt, 32, N=2**14, r=8, p=1)

            # Extract the nonce, tag, and encrypted data
            nonce = enc_data[:12]
            tag = enc_data[12:28]
            encrypted = enc_data[28:]

            # Initialize the AES cipher with the derived key and nonce for GCM mode
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

            # Decrypt the data
            decrypted = cipher.decrypt_and_verify(encrypted, tag)

            return decrypted.decode("utf-8")
        except Exception as e:
            error_message = f"{e}. {traceback.format_exc()}"
            raise Exception(f"Decryption failed: {error_message}")


# Example usage:
key = b"MIIBIjANBgkqhkiG9"
salt = b"lkgmpotomtm"

encryptor_decryptor = AESGCMEncryptorDecryptor(key, salt)
data = "This is a secret message."

try:
    # Encrypt the data
    enc_data = encryptor_decryptor.encrypt_data(data)
    print(f"Encrypted data: {enc_data}")

    # Decrypt the data
    decrypted_data = encryptor_decryptor.decrypt_data(enc_data)
    print(f"Decrypted data: {decrypted_data}")
except Exception as e:
    print(e)
