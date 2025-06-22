"""
Moduł zawierający funkcje kryptograficzne dla Python Secure Messenger.
"""

import os
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def generate_rsa_key_pair():
    """Generuje parę kluczy RSA."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def encrypt_private_key(private_key, password):
    """Szyfruje klucz prywatny hasłem."""
    encrypted_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password.encode())
    )
    return encrypted_key


def decrypt_private_key(encrypted_key, password):
    """Odszyfrowuje klucz prywatny przy użyciu hasła."""
    try:
        private_key = serialization.load_pem_private_key(
            encrypted_key,
            password=password.encode(),
            backend=default_backend()
        )
        return private_key
    except Exception:
        return None


def encrypt_message(message, public_key):
    """
    Szyfruje wiadomość przy użyciu hybrydowego szyfrowania AES+RSA.
    Zwraca zaszyfrowaną wiadomość i zaszyfrowany klucz AES.
    """
    # Generowanie losowego klucza AES i wektora inicjalizacji
    aes_key = os.urandom(32)  # 256 bit
    iv = os.urandom(16)  # 128 bit

    # Szyfrowanie wiadomości przy użyciu AES
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(message.encode()) + encryptor.finalize()

    # Szyfrowanie klucza AES przy użyciu klucza publicznego RSA
    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Łączenie IV z zaszyfrowaną wiadomością
    encrypted_data = iv + encrypted_message

    # Zwracanie zaszyfrowanego klucza AES i zaszyfrowanych danych jako base64
    return base64.b64encode(encrypted_aes_key).decode(), base64.b64encode(encrypted_data).decode()


def decrypt_message(encrypted_data, encrypted_aes_key, private_key):
    """
    Odszyfrowuje wiadomość przy użyciu prywatnego klucza RSA i zaszyfrowanego klucza AES.
    """
    try:
        # Dekodowanie z base64
        encrypted_data = base64.b64decode(encrypted_data)
        encrypted_aes_key = base64.b64decode(encrypted_aes_key)

        # Odszyfrowywanie klucza AES
        aes_key = private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Wyodrębnianie IV i zaszyfrowanej wiadomości
        iv = encrypted_data[:16]
        encrypted_message = encrypted_data[16:]

        # Odszyfrowywanie wiadomości
        cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()

        return decrypted_message.decode()
    except Exception as e:
        print(f"Błąd podczas odszyfrowywania: {e}")
        return None