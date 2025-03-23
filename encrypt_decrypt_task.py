from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

"""

This script provides a class for securely encrypting and decrypting integer values 
using AES-256 encryption in CBC mode. It also includes secure memory handling 
to wipe sensitive data from memory after use.

"""

class EncryptDecryptIntegerUnity:
    def __init__(self):
        self.key = os.urandom(32)  # AES-256 key
        self.iv = os.urandom(16)   # Initialization vector
    
    def secure_wipe(self, data):
        
        """Securely overwrite memory to remove sensitive data."""
        
        if isinstance(data, bytearray):  # For mutable byte arrays
            for i in range(len(data)):
                data[i] = 0
        elif isinstance(data, bytes):  # For immutable bytes
            mutable_data = bytearray(data)
            for i in range(len(mutable_data)):
                mutable_data[i] = 0
            del mutable_data  # Delete the original data
        elif isinstance(data, memoryview):
            data.release()
        del data

    def encrypt_integer_secure(self, value):
        
        """Encrypt an integer securely using AES-256 encryption."""
        
        backend = default_backend()
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=backend)
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        value_bytes = value.to_bytes(5, byteorder='big', signed=True)
        padded_data = padder.update(value_bytes) + padder.finalize()

        # Encrypt the data
        encrypted_value = encryptor.update(padded_data) + encryptor.finalize()

        # Securely wipe memory
        self.secure_wipe(value_bytes)
        self.secure_wipe(padded_data)

        return encrypted_value

    def decrypt_integer_secure(self, encrypted_value):
        
        """Decrypt an encrypted integer securely."""
        
        backend = default_backend()
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=backend)
        decryptor = cipher.decryptor()

        decrypted_padded_value = decryptor.update(encrypted_value) + decryptor.finalize()
    
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_value = unpadder.update(decrypted_padded_value) + unpadder.finalize()

        # Securely wipe memory
        self.secure_wipe(decrypted_padded_value)

        return int.from_bytes(decrypted_value, byteorder='big', signed=True)


if __name__ == "__main__":
    EncryptDecryptIntegerUnity()
