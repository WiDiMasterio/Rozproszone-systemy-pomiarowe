# Laboratorium z rozproszonych systemów pomiarowych

## Opis systemy
System pomiarowy składa się z następujących warstw:

1. Urządzenie końcowe - ESP32 pobiera dane z czujników i publikuje przez WiFi dane na odpowiedni topic MQTT (patrz message_contract.md po więcej szczegółów)
2. MQTT Broker - służy do publikacji pomiarów
3. Ingestor - program, który subskrybuje odpowiednie topiki. Kiedy pojawiają sie na nich nowe dane, sprawdza ich poprawność z obowiązującym kontraktem i przekazuje je do bazy danych
4. Baza danych - postawiona na PostgreSQL magazynuje dane przekazane przez ingestor oraz umożliwia odczytanie ich przez API
5. REST API - udostępnia dane z bazy dla kolejnych warstw progrmów np. do prezentacji
6. Flask - program umożliwiający prezentację zebranych wyników przy pomocy strony internetowej