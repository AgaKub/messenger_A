"""
Python Secure Messenger
-----------------------
Aplikacja do bezpiecznej, szyfrowanej wymiany wiadomości.
"""

import os
import getpass
import user_manager
import message_manager
import config

# Globalne zmienne dla aktualnie zalogowanego użytkownika
current_user = None
current_user_private_key = None


def clear_screen():
    """Czyści ekran konsoli."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Wyświetla nagłówek aplikacji."""
    clear_screen()
    print("Python Secure Messenger")
    print("=" * 24)
    if current_user:
        print(f"Zalogowany jako: {current_user}")
    print()


def register_user():
    """Rejestracja nowego użytkownika."""
    print_header()
    print("Rejestracja nowego użytkownika")
    print("-" * 24)

    username = input("Podaj nazwę użytkownika: ")

    # Sprawdzenie czy użytkownik już istnieje
    if user_manager.user_exists(username):
        print(f"Użytkownik {username} już istnieje!")
        input("Naciśnij Enter, aby kontynuować...")
        return

    # Podanie i potwierdzenie hasła
    password = getpass.getpass("Podaj hasło: ")
    confirm_password = getpass.getpass("Potwierdź hasło: ")

    if password != confirm_password:
        print("Hasła nie pasują do siebie!")
        input("Naciśnij Enter, aby kontynuować...")
        return

    # Tworzenie użytkownika
    success = user_manager.create_user(username, password)

    if success:
        print(f"Użytkownik {username} został pomyślnie zarejestrowany!")
    else:
        print("Wystąpił błąd podczas rejestracji użytkownika.")

    input("Naciśnij Enter, aby kontynuować...")


def login_user():
    """Logowanie użytkownika."""
    global current_user, current_user_private_key

    print_header()
    print("Logowanie użytkownika")
    print("-" * 24)

    username = input("Podaj nazwę użytkownika: ")

    # Sprawdzenie czy użytkownik istnieje
    if not user_manager.user_exists(username):
        print(f"Użytkownik {username} nie istnieje!")
        input("Naciśnij Enter, aby kontynuować...")
        return

    # Podanie hasła
    password = getpass.getpass("Podaj hasło: ")

    # Uwierzytelnianie
    private_key = user_manager.authenticate_user(username, password)

    if private_key:
        current_user = username
        current_user_private_key = private_key
        print(f"Zalogowano pomyślnie jako {username}!")
    else:
        print("Logowanie nieudane!")

    input("Naciśnij Enter, aby kontynuować...")


def logout_user():
    """Wylogowanie użytkownika."""
    global current_user, current_user_private_key

    current_user = None
    current_user_private_key = None

    print("Wylogowano pomyślnie!")
    input("Naciśnij Enter, aby kontynuować...")


def compose_message():
    """Komponowanie i wysyłanie nowej wiadomości."""
    global current_user, current_user_private_key

    print_header()
    print("Nowa wiadomość")
    print("-" * 24)

    # Pobieranie listy wszystkich użytkowników
    all_users = user_manager.get_users()
    all_usernames = [user['username'] for user in all_users]

    # Usunięcie bieżącego użytkownika z listy
    if current_user in all_usernames:
        all_usernames.remove(current_user)

    # Wyświetlanie listy dostępnych odbiorców
    print("Dostępni odbiorcy:")
    for i, username in enumerate(all_usernames, 1):
        print(f"{i}. {username}")

    # Wybór odbiorcy
    choice = input("\nWybierz numer odbiorcy (lub wpisz 'q', aby wrócić): ")

    if choice.lower() == 'q':
        return

    try:
        recipient_index = int(choice) - 1
        if recipient_index < 0 or recipient_index >= len(all_usernames):
            print("Nieprawidłowy numer odbiorcy!")
            input("Naciśnij Enter, aby kontynuować...")
            return

        recipient = all_usernames[recipient_index]
    except ValueError:
        print("Nieprawidłowy wybór!")
        input("Naciśnij Enter, aby kontynuować...")
        return

    # Wprowadzanie treści wiadomości
    print(f"\nKomponowanie wiadomości do {recipient}:")
    print("(Zakończ wiadomość pustą linią)")

    message_lines = []
    while True:
        line = input()
        if not line:
            break
        message_lines.append(line)

    if not message_lines:
        print("Wiadomość jest pusta!")
        input("Naciśnij Enter, aby kontynuować...")
        return

    message = "\n".join(message_lines)

    # Wysyłanie wiadomości
    success = message_manager.send_message(current_user, current_user_private_key, recipient, message)

    if success:
        print(f"Wiadomość została pomyślnie wysłana do {recipient}!")
    else:
        print("Wystąpił błąd podczas wysyłania wiadomości.")

    input("Naciśnij Enter, aby kontynuować...")


def inbox():
    """Przeglądanie skrzynki odbiorczej."""
    global current_user, current_user_private_key

    print_header()
    print("Skrzynka odbiorcza")
    print("-" * 24)

    # Pobieranie wiadomości
    messages = message_manager.get_messages_for_user(current_user)

    if not messages:
        print("Brak wiadomości w skrzynce odbiorczej.")
        input("Naciśnij Enter, aby kontynuować...")
        return

    # Wyświetlanie listy wiadomości
    print(f"Liczba wiadomości: {len(messages)}\n")

    for i, message_data in enumerate(messages, 1):
        sender = message_data['sender']
        timestamp = message_data['timestamp']
        read_status = "Przeczytana" if message_data['read'] else "Nieprzeczytana"

        import datetime
        date_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        print(f"{i}. Od: {sender} | Data: {date_str} | Status: {read_status}")

    # Wybór wiadomości do odczytania
    choice = input("\nWybierz numer wiadomości do odczytania (lub wpisz 'q', aby wrócić): ")

    if choice.lower() == 'q':
        return

    try:
        message_index = int(choice) - 1
        if message_index < 0 or message_index >= len(messages):
            print("Nieprawidłowy numer wiadomości!")
            input("Naciśnij Enter, aby kontynuować...")
            return

        selected_message = messages[message_index]
    except ValueError:
        print("Nieprawidłowy wybór!")
        input("Naciśnij Enter, aby kontynuować...")
        return

    # Odczytywanie wiadomości
    print("\nOdczytywanie wiadomości:")
    print("-" * 24)
    print(f"Od: {selected_message['sender']}")

    import datetime
    date_str = datetime.datetime.fromtimestamp(selected_message['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
    print(f"Data: {date_str}")

    # Odszyfrowanie i wyświetlenie treści
    decrypted_message = message_manager.read_message(selected_message, current_user_private_key)

    if decrypted_message:
        print("\nTreść:")
        print(decrypted_message)
    else:
        print("\nNie udało się odczytać treści wiadomości.")

    input("\nNaciśnij Enter, aby kontynuować...")


def main_menu():
    """Wyświetla menu główne."""
    print_header()
    print("Menu główne")
    print("-" * 24)

    if current_user:
        print("1. Wyślij nową wiadomość")
        print("2. Przeglądaj skrzynkę odbiorczą")
        print("3. Wyloguj się")
    else:
        print("1. Zaloguj się")
        print("2. Zarejestruj nowego użytkownika")

    print("0. Wyjście")

    choice = input("\nWybierz opcję: ")

    if current_user:
        if choice == '1':
            compose_message()
        elif choice == '2':
            inbox()
        elif choice == '3':
            logout_user()
        elif choice == '0':
            return False
    else:
        if choice == '1':
            login_user()
        elif choice == '2':
            register_user()
        elif choice == '0':
            return False

    return True


def main():
    """Funkcja główna aplikacji."""
    # Inicjalizacja konfiguracji
    user_manager.initialize_config()

    running = True
    while running:
        running = main_menu()

    print("Dziękujemy za korzystanie z Python Secure Messenger!")


if __name__ == "__main__":
    main()