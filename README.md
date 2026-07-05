# Generator kodu do serializacji danych sensora

Projekt pokazuje, jak bez użycia AI można zbudować prosty generator kodu w Pythonie. Na podstawie pliku `interface.json` narzędzie generuje klasy serializujące i deserializujące dane do formatu binarnego za pomocą szablonów Jinja2.

## Temat przykładu

W aktualnej wersji projekt jest oparty na scenariuszu „czujnik → odbiornik”.
Czujnik wysyła pomiar przez TCP/IP, a odbiornik odbiera go i wysyła potwierdzenie.
Dane obejmują:
- identyfikator czujnika
- lokalizację
- temperaturę
- wilgotność
- znacznik czasu
- poziom baterii
- historię pomiarów w postaci listy wartości

## Najnowsze funkcje

- generator kodu z pliku `interface.json`
- automatyczna generacja klas `SensorReading` i `ReceiverAck`
- obsługa pól listowych, takich jak `history`
- komunikacja przez TCP/IP między klientem a serwerem
- prosty interfejs GUI w Tkinter w kolorach FC Barcelony
- testy automatyczne dla generatora i GUI

## Struktura projektu

- `interface.json` – definicja struktur danych
- `templates/protocol.py.j2` – szablon Jinja2
- `generator.py` – generator kodu
- `generated_protocol.py` – wygenerowana implementacja
- `server.py` – odbiornik TCP
- `client.py` – czujnik TCP
- `gui_app.py` – interfejs graficzny
- `test_generator.py` – test generatora
- `test_gui_app.py` – test GUI
- `requirements.txt` – zależności projektu

## Jak uruchomić

1. Zainstaluj zależności:

```powershell
python -m pip install -r requirements.txt
```

2. Wygeneruj kod:

```powershell
python generator.py
```

3. Uruchom odbiornik w jednym terminalu:

```powershell
python server.py
```

4. Uruchom czujnik w drugim terminalu:

```powershell
python client.py
```

5. Opcjonalnie uruchom GUI:

```powershell
python gui_app.py
```

## Jak działa projekt

- plik `interface.json` definiuje schemat danych
- `generator.py` wczytuje go i renderuje szablon Jinja2
- wynik jest zapisywany do `generated_protocol.py`
- klasy wygenerowane z tego pliku potrafią:
  - serializować obiekty do bajtów
  - deserializować bajty z powrotem do obiektów
- klient i serwer komunikują się przez TCP/IP i wymieniają dane telemetryczne

## Testy

Uruchom testy poleceniem:

```powershell
python -m pytest -q
```

Jeśli chcesz, można jeszcze rozbudować projekt o:
- wiele czujników jednocześnie
- alarm przy zbyt wysokiej temperaturze
- zapis danych do pliku lub bazy
