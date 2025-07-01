# Dokumentacja – wersja Aga

Komentarz wstępny:  
Ten plik zawiera moją osobistą dokumentację procesu tworzenia aplikacji. Aby poprawnie zrozumieć etapy i sposób pracy, uwzględniam również logikę działania na poziomie konsoli. Moja wersja dokumentacji przedstawia projekt krok po kroku — jako całościowy plan aplikacji opartej na Django z przyszłym systemem szyfrowania.

---

## Etap 1 – Inicjalizacja projektu Django

Cel: Utworzenie szkieletu projektu Django

Wykonane kroki:
- django-admin startproject messenger_project
- python manage.py startapp messenger
- Rejestracja aplikacji `messenger` w `settings.py`
- Utworzenie pliku `projekt-dokumentacja.md` (ta wersja to równoległy dokument: `projekt-dokumentacja-aga.md`)

---

## Etap 2 – Modele i baza danych

Cel: Zbudowanie struktury danych

Plany:
1. Model użytkownika
2. Model wiadomości
3. Model rozmowy (thread)
4. Relacje między nimi
5. Migracje (makemigrations, migrate)

---

## Etap 3 – API (widoki, routing, serializacja)

Cel: Udostępnienie danych przez API

Plany:
1. Widoki typu APIView lub ViewSet
2. Serializery (MessageSerializer, UserSerializer)
3. Routing w urls.py
4. Testowanie endpointów (np. w Postmanie)

---

## Etap 4 – Szyfrowanie wiadomości

Cel: Zabezpieczenie danych użytkownika

Plany:
1. Wybór algorytmu (symetryczne lub asymetryczne)
2. Obsługa kluczy (foldery keys/private/ i keys/public/)
3. Zapisywanie i odczyt kluczy użytkowników
4. Szyfrowanie wiadomości przed zapisem
5. Deszyfrowanie przy odczycie

---

## Etap 5 – Frontend (opcjonalny)

Cel: Dodanie interfejsu użytkownika

Opcje:
1. Frontend oparty na Django (klasyczne widoki i szablony HTML)
2. Prosty frontend konsolowy na potrzeby testów

---

## Etap 6 – Testy i refaktoryzacja

Cel: Uporządkowanie projektu i zapewnienie stabilności

Zadania:
1. Pisanie testów jednostkowych (np. dla modeli i widoków)
2. Refaktoryzacja kodu
3. Przygotowanie do ewentualnego wdrożenia

---

Uwaga końcowa:  
Dokument ten ma być moją logiczną mapą projektu — pisaną moim językiem. Jeśli okaże się, że Grzesiek lepiej rozumie projekt inaczej, możemy pracować równolegle na dwóch wersjach dokumentacji i zsynchronizować się w dowolnym momencie.
