# Struktura kontraktu

#Konrtakt MQTT V1
## Topic
Topic składa się z następujących członów
 - standardowy prefix - lab/g03
 - identyfikator UUIDv4 urządzenia 
 - klasa danych (sensory, wiadomosci błędu)
 - \* dla sensorów nazwa sensora

Przyklad
```
lab/g03/35589507-be86-4a21-a68c-c5fcc1d3a436/sensors/"nazwa sensora" 
lab/g03/35589507-be86-4a21-a68c-c5fcc1d3a436/errorMsg
```

## Payloady
### Payload dla sensorów
Pola wymagane 
- ts_ms: int - czas od uruchomienia plytki
- device_name: String - nazwa huba/plytki
- description: String - opis pomiaru np. "temp"
- value: float - wartość pomiaru
- unit: String - jednostka wartości mierzonej
- msgIdx : int - indeks wiadomości

Pola opcjonalne
- UUIDv4: String - UUID urządzenia

Przykładowy payload:
```
message = {
    "ts_ms": 32143,
    "device_name": "espSalon",
    "description": "distance",
    "value": 23.45,
    "unit": "cm",
    "msgIdx": 4,
    "UUIDv4": "35589507-be86-4a21-a68c-c5fcc1d3a436"
}
```

### Payload error message
Pola wymagane
- "ts_ms": int (w ms)
- "errorSource": String - informacja, skąd pochodzi błąd
- "errorMSG": String - główna treść błędu
- "errorIdx": int - indeks errora

## Weryfikacja błędu
* Sprawdzeniu indeksu wiadomości, co pozwala sprawdzić czy nie stracono żadnych wiadomości w trakcie transmisji

* Niezgodność formatu dla danej wiadomości, gdy dana wiadomość nie ma kompletu wymaganych pól, wiadomość jest uznawana za błędną
