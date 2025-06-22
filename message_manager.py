""""
Moduł zarządzania wiadomościami dla Python Secure Messenger.
"""

import os
import json
import time
import uuid
import config
import crypto
import user_manager


def save_message(sender, recipient, encrypted_message, encrypted_key):
    """Zapisuje zaszyfrowaną wiadomość."""
    # Tworzenie unikalnego ID wiadomości
    message_id = str(uuid.uuid4())

    # Przygotowanie danych wiadomości
    message_data = {
        'id': message_id,
        'sender': sender,
        'recipient': recipient,
        'encrypted_message': encrypted_message,
        'encrypted_key': encrypted_key,
        'timestamp': time.time(),
        'read': False
    }

    # Zapisywanie wiadomości do pliku
    message_file = os.path.join(config.MESSAGES_DIR, f"{message_id}.json")
    with open(message_file, 'w') as f:
        json.dump(message_data, f)

    print(f"Wiadomość została pomyślnie zapisana z ID: {message_id}")
    return message_id


def send_message(sender, sender_private_key, recipient, message):
    """Wysyła zaszyfrowaną wiadomość do odbiorcy."""
    # Pobieranie klucza publicznego odbiorcy
    recipient_public_key = user_manager.get_user_public_key(recipient)

    if recipient_public_key is None:
        print(f"Nie można wysłać wiadomości, ponieważ nie znaleziono klucza publicznego odbiorcy {recipient}.")
        return False

    # Szyfrowanie wiadomości
    encrypted_key, encrypted_message = crypto.encrypt_message(message, recipient_public_key)

    # Zapisywanie wiadomości
    message_id = save_message(sender, recipient, encrypted_message, encrypted_key)

    if message_id:
        print(f"Wiadomość została pomyślnie wysłana do {recipient}.")
        return True
    else:
        print("Wystąpił błąd podczas wysyłania wiadomości.")
        return False


def get_messages_for_user(username):
    """Pobiera wszystkie wiadomości dla danego użytkownika."""
    messages = []

    # Przeszukiwanie katalogu wiadomości
    for filename in os.listdir(config.MESSAGES_DIR):
        if not filename.endswith('.json'):
            continue

        message_path = os.path.join(config.MESSAGES_DIR, filename)

        with open(message_path, 'r') as f:
            message_data = json.load(f)

        # Dodawanie wiadomości, jeśli jest przeznaczona dla tego użytkownika
        if message_data['recipient'] == username:
            messages.append(message_data)

    # Sortowanie wiadomości według czasu
    messages.sort(key=lambda x: x['timestamp'])

    return messages


def read_message(message_data, private_key):
    """Odczytuje zaszyfrowaną wiadomość przy użyciu klucza prywatnego."""
    encrypted_message = message_data['encrypted_message']
    encrypted_key = message_data['encrypted_key']

    # Odszyfrowywanie wiadomości
    decrypted_message = crypto.decrypt_message(encrypted_message, encrypted_key, private_key)

    if decrypted_message:
        # Oznaczanie wiadomości jako przeczytanej
        message_data['read'] = True
        message_path = os.path.join(config.MESSAGES_DIR, f"{message_data['id']}.json")

        with open(message_path, 'w') as f:
            json.dump(message_data, f)

        return decrypted_message
    else:
        print("Nie udało się odszyfrować wiadomości.")
        return None