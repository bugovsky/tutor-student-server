# Серверная часть приложения TutorStudentApp

## Инструкция по развертыванию

1. Склонировать репозиторий
2. Перейти в папку проекта (`your_path/tutor-student-server`)
3. Создать `.env` файл и указать в нем следующие поля и присвоить им значения:
    ```text
    DATABASE_HOST = 
    DATABASE_PORT = 
    DATABASE_PASSWORD = 
    DATABASE_NAME = 
    DATABASE_USERNAME = 
    SECRET_KEY = 
    ALGORITHM = 
    ACCESS_TOKEN_EXPIRE_MINUTES = 
    YANDEX_DISK_TOKEN = 
    ```
4. Выполнить команду в терминале `docker-compose up --build`. 

   При повтором запуске достаточно выполнить `docker-compose up`.