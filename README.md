# Generator kodu do serializacji TCP/IP

Projekt pokazuje generator kodu opartego na Jinja2, który z pliku `interface.json` tworzy Pythonowy moduł `generated_protocol.py` z metodami `serialize()` i `deserialize_from()`.

## Struktura

- `interface.json` - definicja struktur danych
- `templates/protocol.py.j2` - szablon Jinja2
- `generator.py` - generator kodu
- `generated_protocol.py` - wygenerowana implementacja
- `server.py` - prosty serwer TCP
- `client.py` - prosty klient TCP

## Jak używać

1. Zainstaluj zależności:

```bash
python -m pip install jinja2
```

2. Wygeneruj kod:

```bash
python generator.py
```

3. Uruchom serwer:

```bash
python server.py
```

4. W innym terminalu uruchom klienta:

```bash
python client.py
```

## Jak działa

- `ChatMessage` i `Ack` są serializowane do binarnego formatu:
  - string: długość `uint32` + dane UTF-8
  - integer: mały pakiet `struct`
- klient wysyła `ChatMessage`, serwer odsyła `Ack`
