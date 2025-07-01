# Dokumentacja – wersja Aga

Komentarz wstępny:  
Ten plik zawiera moją osobistą dokumentację procesu tworzenia aplikacji. Aby poprawnie zrozumieć etapy i sposób pracy, uwzględniam również logikę działania na poziomie konsoli. Moja wersja dokumentacji przedstawia projekt krok po kroku — jako całościowy plan aplikacji opartej na Django z przyszłym systemem szyfrowania.
Dokument ten ma być moją logiczną mapą projektu — pisaną moim językiem. Jeśli okaże się, że Grzesiek lepiej rozumie projekt inaczej, możemy pracować równolegle na dwóch wersjach dokumentacji i zsynchronizować się w dowolnym momencie.

# Secure Messenger – wersja Django

## 1. Wprowadzenie

- **Nazwa projektu**: Secure Messenger – wersja Django  
- **Cel**: Przeniesienie komunikatora z wersji konsolowej do webowej, z zachowaniem szyfrowania wiadomości.  
- **Mój wkład**: Dokumentacja krok po kroku, porządkowanie logiki projektu, przygotowanie do dalszego rozwoju.  
- **Dlaczego ten projekt**: Chcę pokazać, jak uczę się strukturalnie i dokumentuję myślenie, nie tylko efekt końcowy.

## 2. Środowisko i instalacja

- **Wersja Pythona**: 3.x  
- **Wirtualne środowisko**: utworzone lokalnie, aktywowane przez `venv`  
- **Instalacja bibliotek**:

pip install django cryptography

- **Struktura folderów projektu**:
messenger/
├── config/ # konfiguracja Django
├── keys/ # klucze szyfrujące
├── messages/ # wiadomości
├── test/ # pliki testowe
├── .idea/ # pliki środowiskowe IDE
├── config.py # główna konfiguracja aplikacji
├── crypto.py # moduł szyfrowania
├── message_manager.py # obsługa wiadomości
├── user_manager.py # zarządzanie użytkownikami
└── secure_messenger.py # wersja konsolowa


## 3. Logika projektu

- Komunikator szyfruje wiadomości, umożliwia przesyłanie i odczyt tylko autoryzowanym użytkownikom.  
- **Moduły**:
- `crypto.py`: generowanie i ładowanie kluczy, szyfrowanie/odszyfrowywanie
- `message_manager.py`: logika obsługi wiadomości (dodawanie, lista, odszyfrowanie)
- `user_manager.py`: zarządzanie użytkownikami
- **Szyfrowanie**: oparte na bibliotece `cryptography`, używa kluczy `.key` przechowywanych lokalnie  
- **Plany rozwoju**: rozbudowa o backend Django i interfejs webowy

## 4. Etapy migracji (konsola → Django)

- Początkowa wersja to skrypt konsolowy z szyfrowaniem wiadomości
- Migracja objęła:
- przeniesienie logiki do aplikacji Django
- uporządkowanie plików i podział na foldery
- wstępne przygotowanie do integracji z interfejsem webowym
- **Optymalizacje**:
- Rozdzielenie ról plików
- Uproszczenie logiki dodawania wiadomości

## 5. Mój sposób dokumentowania

- Prowadzę **własną dokumentację**: wersja krok po kroku, aby nie zginąć w chaosie podczas nauki  
- **Język dokumentacji**: logiczny, strukturalny, oparty na pytaniach typu: *co robi ten plik?*, *co testuje ta metoda?*, *czy to działa niezależnie?*  
- **Dlaczego osobna wersja**:
- Każdy myśli trochę inaczej – zachowuję porządek dostosowany do mojego stylu pracy
- Chcę zostawić ślad procesu nauki, nie tylko gotowy efekt

## 6. Plany na rozwój

- Rejestracja i logowanie użytkownika
- Interfejs webowy z listą wiadomości
- Historia rozmów i baza danych
- Uwierzytelnianie i kontrola dostępu
- Testy jednostkowe i integracyjne
- Wersja demo do testów z użytkownikiem

---

> _Dokumentacja prowadzona przez Agnieszke Kubczak w ramach nauki Django i bezpiecznego przesyłania danych w aplikacjach webowych._

