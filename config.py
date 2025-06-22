"""
Plik konfiguracyjny dla Python Secure Messenger.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
KEYS_DIR = os.path.join(BASE_DIR, 'keys')
PUBLIC_KEYS_DIR = os.path.join(KEYS_DIR, 'public')
PRIVATE_KEYS_DIR = os.path.join(KEYS_DIR, 'private')
MESSAGES_DIR = os.path.join(BASE_DIR, 'messages')


USER_CONFIG_FILE = os.path.join(CONFIG_DIR, 'users.json')

RSA_KEY_SIZE = 2048  # Rozmiar klucza RSA
AES_KEY_SIZE = 256   # Rozmiar klucza AES