from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

KEY_DERIVATION = HKDF(
    algorithm=hashes.SHA256(),
    length=16,
    salt=None,
    info=b""
)


class AES():
    def __init__(self, diffie_hellman_key: int) -> None:

        key_in_bytes = diffie_hellman_key.to_bytes(
            (diffie_hellman_key.bit_length() + 7) // 8)

        # Converts the DH key to a suitable one for AES
        self.symmetric_key = KEY_DERIVATION.derive(key_in_bytes)

    def encrypt(self, message: str) -> bytes:
        # This is used so that the same plaintext with the same key generates the same key
        message_bytes = message.encode()
        message_bytes = AES.__pad(message_bytes)
        iv = os.urandom(16)

        cipher = Cipher(algorithms.AES(self.symmetric_key),
                        modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()  # The encryptor using AES-128

        ciphertext = encryptor.update(message_bytes) + encryptor.finalize()

        return iv + ciphertext

    def decrypt(self, message: bytes) -> str:
        iv = message[:16]
        ciphertext = message[16:]

        cipher = Cipher(algorithms.AES(self.symmetric_key),
                        modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted_bytes = decryptor.update(ciphertext) + decryptor.finalize()

        decrypted_string = AES.__unpad(decrypted_bytes).decode('utf-8')

        return decrypted_string

    @staticmethod
    def __pad(data: bytes) -> bytes:
        padding_length = 16 - (len(data) % 16)

        padding = bytes([padding_length] * padding_length)

        return data + padding

    @staticmethod
    def __unpad(padded_data: bytes) -> bytes:  # Inverse of __pad (adheres to PKCS#7)
        padding_length = padded_data[-1]

        return padded_data[:-padding_length]
