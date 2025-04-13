# urban-memory
API-сервис бронирования столиков в ресторане

<br>
Столики:
<br>
GET /tables/ — список всех столиков<br>
POST /tables/ — создать новый столик<br>
DELETE /tables/{id} — удалить столик<br>
<br>

![add_table1](https://github.com/user-attachments/assets/ffe0e278-3613-4b1b-901d-e0cd9bfac426)

<br>
Брони:
<br>
GET /reservations/ — список всех броней<br>
POST /reservations/ — создать новую бронь<br>
DELETE /reservations/{id} — удалить бронь<br>
<br>

![reserve_in_base](https://github.com/user-attachments/assets/007014ea-1d6d-4b03-9124-c63938942928)

<br>
Собрать и запустить контейнеры:
<br>
docker-compose up -d --build
<br>
Пересобрать образ и очистить кэш:
<br>
docker-compose down -v
docker-compose build --no-cache
docker-compose up
<br>
Приложение запускается в: http://localhost:8000
<br>
Docs:  http://localhost:8000/docs
<br>

![docs](https://github.com/user-attachments/assets/d5c4ae21-239b-4758-879d-6643d3c4a08d)

<br>
redoc: http://localhost:8000/redoc
<br>

![redoc](https://github.com/user-attachments/assets/1b00be41-2904-4d28-96a2-553bd8a67c89)

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
