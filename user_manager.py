"""
Moduł zarządzania użytkownikami dla Python Secure Messenger.
"""

import os
import json
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import config
import crypto


def initialize_config():
    """Inicjalizacja plików konfiguracyjnych."""
    # Upewnienie się, że katalogi istnieją
    for directory in [config.CONFIG_DIR, config.KEYS_DIR,
                      config.PUBLIC_KEYS_DIR, config.PRIVATE_KEYS_DIR,
                      config.MESSAGES_DIR]:
        os.makedirs(directory, exist_ok=True)

    # Tworzenie pliku konfiguracyjnego użytkowników, jeśli nie istnieje
    if not os.path.exists(config.USER_CONFIG_FILE):
        with open(config.USER_CONFIG_FILE, 'w') as f:
            json.dump({'users': []}, f)
        print(f"Utworzono plik konfiguracyjny użytkowników.")

    print("Inicjalizacja konfiguracji zakończona pomyślnie!")


def get_users():
    """Pobiera listę wszystkich użytkowników."""
    if not os.path.exists(config.USER_CONFIG_FILE):
        return []

    with open(config.USER_CONFIG_FILE, 'r') as f:
        users_data = json.load(f)

    return users_data.get('users', [])


def user_exists(username):
    """Sprawdza czy użytkownik o danej nazwie istnieje."""
    users = get_users()
    return any(user['username'] == username for user in users)


def create_user(username, password):
    """Tworzy nowego użytkownika z parą kluczy."""
    if user_exists(username):
        print(f"Użytkownik {username} już istnieje!")
        return False

    # Generowanie kluczy
    private_key, public_key = crypto.generate_rsa_key_pair()

    # Szyfrowanie klucza prywatnego hasłem
    encrypted_private_key = crypto.encrypt_private_key(private_key, password)

    # Eksport klucza publicznego
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Zapisywanie kluczy do plików
    private_key_path = os.path.join(config.PRIVATE_KEYS_DIR, f"{username}.pem")
    public_key_path = os.path.join(config.PUBLIC_KEYS_DIR, f"{username}.pem")

    with open(private_key_path, 'wb') as f:
        f.write(encrypted_private_key)

    with open(public_key_path, 'wb') as f:
        f.write(public_key_bytes)

    # Dodawanie użytkownika do pliku konfiguracyjnego
    users = get_users()
    users.append({
        'username': username,
        'private_key_path': private_key_path,
        'public_key_path': public_key_path
    })

    with open(config.USER_CONFIG_FILE, 'w') as f:
        json.dump({'users': users}, f)

    print(f"Użytkownik {username} został pomyślnie utworzony!")
    return True


def get_user_public_key(username):
    """Pobiera klucz publiczny użytkownika."""
    if not user_exists(username):
        print(f"Użytkownik {username} nie istnieje!")
        return None

    public_key_path = os.path.join(config.PUBLIC_KEYS_DIR, f"{username}.pem")

    if not os.path.exists(public_key_path):
        print(f"Klucz publiczny dla użytkownika {username} nie istnieje!")
        return None

    with open(public_key_path, 'rb') as f:
        public_key_bytes = f.read()

    public_key = serialization.load_pem_public_key(
        public_key_bytes,
        backend=default_backend()
    )

    return public_key


def authenticate_user(username, password):
    """Uwierzytelnia użytkownika przy użyciu hasła."""
    if not user_exists(username):
        print(f"Użytkownik {username} nie istnieje!")
        return None

    private_key_path = os.path.join(config.PRIVATE_KEYS_DIR, f"{username}.pem")

    if not os.path.exists(private_key_path):
        print(f"Klucz prywatny dla użytkownika {username} nie istnieje!")
        return None

    with open(private_key_path, 'rb') as f:
        encrypted_private_key = f.read()

    private_key = crypto.decrypt_private_key(encrypted_private_key, password)

    if private_key is None:
        print("Nieprawidłowe hasło!")
        return None

    print(f"Użytkownik {username} został pomyślnie uwierzytelniony!")
    return private_key