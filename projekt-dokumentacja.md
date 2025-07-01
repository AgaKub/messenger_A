# Dokumentacja projektu Python Secure Messenger

## 1. Przygotowanie środowiska 

### Instalacja niezbędnych bibliotek (cryptography)

No więc na początku musiałem zainstalować bibliotekę `cryptography`, bo bez niej ciężko byłoby zrobić bezpieczny komunikator. Ta biblioteka ma wszystko czego potrzebujemy do szyfrowania.

```python
# Instalacja przez pip
pip install cryptography
```

Wybrałem cryptography, bo jest prosta w użyciu i ma wszystkie potrzebne algorytmy już gotowe. Nie chciało mi się pisać własnych implementacji RSA czy AES, bo to by zajęło wieki, a pewnie i tak bym popełnił jakieś błędy bezpieczeństwa.

### Utworzenie struktury katalogów projektu (keys, messages, etc.)

Żeby zachować jakiś porządek, stworzyłem taką strukturę folderów:
 
#### Utwórz główny katalog projektu

mkdir python-secure-messenger

cd python-secure-messenger

#### Utwórz podkatalogi

mkdir config

mkdir keys

mkdir "keys\private"

mkdir "keys\public"

mkdir messages

```
python-secure-messenger/
├── config/                   # Tu będą pliki konfiguracyjne
├── keys/                     # Katalog na klucze
│   ├── private/              # Klucze prywatne (zaszyfrowane)
│   └── public/               # Klucze publiczne (niezaszyfrowane)
├── messages/                 # Tu będą zapisywane zaszyfrowane wiadomości
├── config.py                 # Plik z ustawieniami
├── crypto.py                 # Funkcje do szyfrowania/deszyfrowania
├── user_manager.py           # Zarządzanie użytkownikami
├── message_manager.py        # Zarządzanie wiadomościami
└── secure_messenger.py       # Główny plik aplikacji
```

Rozdzieliłem to na kilka modułów, żeby łatwiej się pracowało i nie było jednego wielkiego pliku ze wszystkim.

### Inicjalizacja podstawowych plików konfiguracyjnych

Zrobiłem plik `config.py`, który trzyma ścieżki do katalogów i różne ustawienia:

```python
import os

# Ścieżki do folderów
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
KEYS_DIR = os.path.join(BASE_DIR, 'keys')
PUBLIC_KEYS_DIR = os.path.join(KEYS_DIR, 'public')
PRIVATE_KEYS_DIR = os.path.join(KEYS_DIR, 'private')
MESSAGES_DIR = os.path.join(BASE_DIR, 'messages')

# Pliki konfiguracyjne
USER_CONFIG_FILE = os.path.join(CONFIG_DIR, 'users.json')

# Ustawienia kryptograficzne
RSA_KEY_SIZE = 2048  # Klucz 2048 bitów powinien być wystarczająco bezpieczny
AES_KEY_SIZE = 256   # A tu 256 bitów
```

W folderze `config` trzymam plik `users.json`, który przechowuje info o użytkownikach. Przy pierwszym uruchomieniu aplikacji inicjalizuję go tak:

```python
def initialize_config():
    # Upewniam się, że katalogi istnieją
    for directory in [CONFIG_DIR, KEYS_DIR, PUBLIC_KEYS_DIR, PRIVATE_KEYS_DIR, MESSAGES_DIR]:
        os.makedirs(directory, exist_ok=True)
    
    # Tworzę plik users.json jeśli nie istnieje
    if not os.path.exists(USER_CONFIG_FILE):
        with open(USER_CONFIG_FILE, 'w') as f:
            json.dump({'users': []}, f)
        print(f"Utworzyłem plik konfiguracyjny użytkowników.")
```

## 2. Implementacja zarządzania użytkownikami 

### Tworzenie nowych użytkowników

Tworzenie nowego użytkownika wygląda tak:
- Sprawdzam, czy nazwa użytkownika jest już zajęta
- Biore od użytkownika hasło
- Generuję parę kluczy kryptograficznych
- Zapisuję wszystko do plików

```python
def create_user(username, password):
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
```

### Generowanie par kluczy RSA

Generowanie kluczy RSA to prosta sprawa dzięki bibliotece `cryptography`:

```python
def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # To jest standardowa wartość
        key_size=2048,          # 2048 bitów powinno wystarczyć
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key
```

Można by użyć 4096-bitowych, ale to by zwolniło szyfrowanie, a i tak 2048 jest trudne do złamania.

### Zabezpieczanie kluczy prywatnych hasłem

Klucz prywatny to najważniejsza rzecz do ochrony, więc szyfruję go hasłem użytkownika:

```python
def encrypt_private_key(private_key, password):
    encrypted_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password.encode())
    )
    return encrypted_key
```

Używam algorytmu `BestAvailableEncryption`, który wybiera najlepszy dostępny algorytm na systemie. Format PKCS8 to standard do trzymania kluczy prywatnych.

### Zarządzanie listą dostępnych użytkowników

Muszę jakoś trzymać listę użytkowników, żeby można było wysyłać wiadomości między nimi:

```python
def get_users():
    if not os.path.exists(config.USER_CONFIG_FILE):
        return []
    
    with open(config.USER_CONFIG_FILE, 'r') as f:
        users_data = json.load(f)
    
    return users_data.get('users', [])
```

Przy wysyłaniu wiadomości pokazuję listę dostępnych odbiorców (oczywiście bez obecnie zalogowanego użytkownika, bo nie ma sensu wysyłać wiadomości do samego siebie):

```python
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
```

## 3. Implementacja funkcji kryptograficznych 

### Generowanie kluczy AES dla pojedynczych wiadomości

Używam szyfrowania hybrydowego, bo to najlepszy sposób:
- AES jest szybki, ale wymaga tego samego klucza po obu stronach
- RSA jest wolny, ale pozwala na bezpieczne przesyłanie kluczy

Dlatego dla każdej wiadomości generuję nowy klucz AES:

```python
# Generowanie losowego klucza AES i wektora inicjalizacji
aes_key = os.urandom(32)  # 256 bit - im więcej, tym lepiej
iv = os.urandom(16)       # 128 bit - wymagane przez AES
```

### Szyfrowanie wiadomości algorytmem AES

Wiadomości szyfruję za pomocą AES w trybie CFB:

```python
# Szyfrowanie wiadomości przy użyciu AES
cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
encryptor = cipher.encryptor()
encrypted_message = encryptor.update(message.encode()) + encryptor.finalize()
```

Tryb CFB jest fajny, bo pozwala szyfrować dane bez konieczności dzielenia ich na bloki i nie trzeba dodawać paddingu.

### Szyfrowanie klucza AES kluczem publicznym RSA odbiorcy

Żeby odbiorca mógł odczytać wiadomość, muszę mu jakoś przekazać klucz AES. Robię to szyfrując klucz AES przy użyciu klucza publicznego RSA odbiorcy:

```python
# Szyfrowanie klucza AES przy użyciu klucza publicznego RSA
encrypted_aes_key = public_key.encrypt(
    aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
```

### Funkcje deszyfrowania wiadomości

```python
def decrypt_message(encrypted_data, encrypted_aes_key, private_key):
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
        iv = encrypted_data[:16]  # Pierwsze 16 bajtów to IV
        encrypted_message = encrypted_data[16:]  # Reszta to zaszyfrowana wiadomość
        
        # Odszyfrowywanie wiadomości
        cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
        
        return decrypted_message.decode()
    except Exception as e:
        print(f"Błąd podczas odszyfrowywania: {e}")
        return None
```

## 4. System przechowywania wiadomości 

### Struktura plików JSON do przechowywania zaszyfrowanych wiadomości

Każda wiadomość jest zapisywana jako osobny plik JSON w katalogu `messages/`.

```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "sender": "alice",
    "recipient": "bob",
    "encrypted_message": "base64_encoded_encrypted_message",
    "encrypted_key": "base64_encoded_encrypted_key",
    "timestamp": 1621504890.123456,
    "read": false
}
```

Dzięki temu:
- Każda wiadomość ma unikalny identyfikator (UUID)
- Wiem kto wysłał wiadomość i do kogo
- Przechowuję zaszyfrowaną treść i klucz
- Mam timestamp do sortowania wiadomości
- Wiem, czy wiadomość została przeczytana

### Mechanizm identyfikacji nadawcy i odbiorcy

Dzięki informacjom o nadawcy i odbiorcy mogę łatwo filtrować wiadomości dla konkretnego użytkownika:

```python
def get_messages_for_user(username):
    messages = []
    
    # Przeszukiwanie katalogu wiadomości
    for filename in os.listdir(config.MESSAGES_DIR):
        if not filename.endswith('.json'):
            continue
        
        message_path = os.path.join(config.MESSAGES_DIR, filename)
        
        with open(message_path, 'r') as f:
            message_data = json.load(f)
        
        # Dodawanie wiadomości, jeśli jest dla tego użytkownika
        if message_data['recipient'] == username:
            messages.append(message_data)
    
    # Sortowanie wiadomości wg czasu (od najstarszych)
    messages.sort(key=lambda x: x['timestamp'])
    
    return messages
```

### System oznaczania przeczytanych/nieprzeczytanych wiadomości

Po odczytaniu wiadomości zmieniam jej status na "przeczytana":

```python
def read_message(message_data, private_key):
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
```

Status wiadomości pokazuję w skrzynce odbiorczej, żeby użytkownik wiedział, które wiadomości już przeczytał:

```python
for i, message_data in enumerate(messages, 1):
    sender = message_data['sender']
    timestamp = message_data['timestamp']
    read_status = "Przeczytana" if message_data['read'] else "Nieprzeczytana"
    
    import datetime
    date_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"{i}. Od: {sender} | Data: {date_str} | Status: {read_status}")
```

## 5. Interfejs użytkownika 

### Menu główne aplikacji

Interfejs zrobiłem najprostszy jak się da - tekstowy w konsoli. Menu główne pokazuje różne opcje w zależności od tego, czy użytkownik jest zalogowany czy nie:

```python
def main_menu():
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
    # Obsługa wybranej opcji...
```

### Opcje logowania użytkownika

Logowanie to prosty proces:
- Proszę o nazwę użytkownika
- Sprawdzam czy taki użytkownik istnieje
- Proszę o hasło
- Próbuję odszyfrować klucz prywatny tym hasłem

```python
def login_user():
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
    
    # Podanie hasła (getpass nie pokazuje hasła podczas wpisywania)
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
```

### Funkcje wysyłania nowych wiadomości

Wysyłanie wiadomości działa tak:
- Pokazuję listę dostępnych odbiorców
- Użytkownik wybiera odbiorcę
- Użytkownik wpisuje wiadomość 
- Wiadomość jest szyfrowana i zapisywana

```python
def compose_message():
    global current_user, current_user_private_key
    
    print_header()
    print("Nowa wiadomość")
    print("-" * 24)
    
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
```

### Funkcje odczytywania otrzymanych wiadomości

Odczytywanie wiadomości to:
- Pobranie wiadomości dla zalogowanego użytkownika
- Pokazanie listy wiadomości (nadawca, data, status)
- Wybór wiadomości do odczytania
- Odszyfrowanie i pokazanie treści

```python
def inbox():
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
```

### System informowania o nowych wiadomościach

Przy wejściu do skrzynki pokazuję ile jest nieprzeczytanych wiadomości:

```python
# Pobieranie wiadomości
messages = message_manager.get_messages_for_user(current_user)

# Liczenie nieprzeczytanych wiadomości
unread_count = sum(1 for msg in messages if not msg['read'])

# Wyświetlanie informacji
print(f"Liczba wiadomości: {len(messages)} (Nieprzeczytane: {unread_count})\n")
```



### Moja część (A)

Skupiam się na logice aplikacji:

- Projektowanie **modeli Django** (wiadomości, rozmowy, użytkownicy)
- Tworzenie **widoków API** do obsługi wiadomości
- Planowanie systemu szyfrowania (późniejsze wdrożenie)
- Wstępne testy jednostkowe

---

### Struktura projektu (na tym etapie)

messenger_project/
│
├── messenger/ # Aplikacja Django
│ ├── models.py # Wiadomości, rozmowy
│ ├── views.py # Widoki API
│ ├── urls.py # Routing
│ └── serializers.py # Obsługa danych do/od API
│
├── messenger_project/ # Ustawienia Django
│ ├── settings.py
│ └── urls.py
│
├── manage.py
└── README.md


###  Jak uruchomić lokalnie

```bash
# krok 1 – migracje
python manage.py makemigrations  
python manage.py migrate

# krok 2 – uruchomienie serwera
python manage.py runserver


Plan dalszych kroków, ewentualnie
dodanie prostego szyfrowania wiadomości 

testowanie endpointów API 

stworzenie prostego frontendu (Grzesiek?)

bsługa wątków, kilku rozmów, użytkowników


