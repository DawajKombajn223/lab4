# Generator kodu do serializacji danych sensora

Projekt pokazuje generator kodu opartego na Jinja2, który z pliku `interface.json` tworzy Pythonowy moduł `generated_protocol.py` z metodami `serialize()` i `deserialize_from()`.

## Temat przykładu

W tym wariancie czujnik wysyła pomiar do odbiornika przez TCP/IP. Przykład pokazuje, jak wygenerować kod do serializacji danych telemetrycznych takich jak temperatura, wilgotność i poziom baterii.

## Struktura

- `interface.json` - definicja struktur danych
- `templates/protocol.py.j2` - szablon Jinja2
- `generator.py` - generator kodu
- `generated_protocol.py` - wygenerowana implementacja
- `server.py` - odbiornik TCP
- `client.py` - czujnik TCP

## Jak używać

1. Zainstaluj zależności:

```bash
python -m pip install -r requirements.txt
```

2. Wygeneruj kod:

```bash
python generator.py
```

3. Uruchom odbiornik:

```bash
python server.py
```

4. W innym terminalu uruchom czujnik:

```bash
python client.py
```

## Jak działa

- `SensorReading` i `ReceiverAck` są serializowane do formatu binarnego:
  - string: długość `uint32` + dane UTF-8
  - liczby: pakiet `struct`
- czujnik wysyła pomiar, a odbiornik odsyła potwierdzenie
