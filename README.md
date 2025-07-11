# FastAPI Template Architecture

### Enviroment variables
> Создать файл .env из .env.example и поместить в backend директорию

### Запуск приложения
> python main.py

### Документация 
http://localhost:8001/api/v1/docs

### Разные команды

(параметры запуска для uvicorn)
> --reload --host 0.0.0.0 --port 8001

### Структура директорий

| Описание                        | php            | fastapi_template_architecture |
|---------------------------------|----------------|-------------------------------|
| обработчик                      | controller     | api                           |
| классы валидации входных данных | dto            | schema                        |
| сервисы с бизнес логикой        | service + impl | service                       |
| классы для мапинга              | dao / mapper   | crud                          |
| модели (БД)                     | model / entity | model                         |


### Poetry
```Bash
# Создание requirements.txt экспорта зависимостей без хэшей
poetry export --without-hashes -f requirements.txt --output requirements.txt  

# или аналогичная команда
poetry export --without-hashes --format=requirements.txt > requirements.txt
```

### Docker
```Bash

# Полная пересборка контейнеров со скачиванием всех зависимостей (самый лучший вариант)
docker compose build --no-cache

# Полная пересборка конкретного контейнера
docker compose build --no-cache my_container

# (Пересборка контейнера, принудительная)
docker-compose up --build --force-recreate --renew-anon-volumes --no-cache

# (Сборка контейнеров)
docker-compose build

# (Зайти в конкретный контейнер)
docker exec -ti backend_fastapi_2024 bash

# (Запуск контейнеров в фоне)
docker-compose up -d

# (Вывести список контейнеров остановленных и работающих)
docker ps -a

# Именнные volume (тома) хранятся в windows по пути
\\wsl$\docker-desktop-data\data\docker\volumes
```

### Alembic
```Bash
alembic init migrations
alembic revision --autogenerate -m "init"
alembic upgrade head
alembic history
alembic downgrade 8ac14e223d1e
alembic downgrade -1 (удаление всех миграций)
```

### Minio
Для того что бы работал minio на получение и на загрузку файлов, необходимо
добавить строку (разрешить DNS) в файле hosts (windows/linux):

```
minio - 'название контейнера minio' /
127.0.0.1 - 'адрес хоста (localhost не заработал), сюда нужно будет прописать IP сервера, 
где будет развернуто приложение'

...hosts
127.0.0.1 minio
```  

Файл из минио можно получить так
http://localhost:8001/api/v1/minio/file?file=avatar/71d3de1b-bcef-4f41-8364-2595c2d1adf6.jpg&bucket=images
или через Nginx как обратный реверс прокси
http://localhost:88/images/660c358c-a59a-4b1f-8a12-c853e8ebd065.jpg

### Todo
1. Добавить Celery (+)
2. Фоновые задачи Celery (+)
3. Celery Flower (+)
4. Redis (+)
5. RabbitMQ
6. Миграции Alembic (+)
7. Попробовать пересоздать контейнер на базе Slim (+)
8. CRUD для MongoDB (+)
9. GreadFS для MongoDB
10. Добавить SQLAlchemy (+)
11. Реализовать регистрацию пользователей. (+)
12. Тестирование
13. Добавить роли / права
14. Сделать Тестовой приложение Posts с категориями и тегами

#### PGAdmin
- host name default => db_fastapi_2024
- login => postgres
- password => 123123


#### Testing

1. Создать базу test_db
2. Запуск тестов
```Bash
pytest -vs --disable-warnings
```

3. Запуск алембика для теста
```Bash
alembic -c tests/alembic.ini history
```
4. Создание миграций для тестов
```Bash
alembic -c tests/alembic.ini revision --autogenerate -m "init"
```
5. Запуск тестов
```Bash
pytest -v --pyargs tests --capture=no
```
- флаг --capture=no включает вывод логирования в консоль. (использовать при отладке)
6. Запуск тестов с отключением warning предупреждений
```Bash
pytest -v --disable-warnings
```

7.Запуск всез тестов через Docker
```Bash
docker-compose exec backend_fastapi_2024 python -m pytest tests/api_v1/ -v --tb=short
```

#### Celery


```Bash
# Scheduled tasks (optional)
celery -A backend.task.celery beat -l info

# Run only worker
celery -A backend.task.celery worker -l info

# Run 'Worker' and 'Beat' Scheduled tasks (optional). Show result in console. Use ONLY DEVELOPER!
celery -A backend.task.celery worker -l info -B

# Web monitor (optional)
celery -A task.celery flower --port=8555 --basic-auth=admin:123456

# logout basic auth from celery flower
http://exit:exit@localhost:8555/
```

#### Mongo

```Bash
# Connection string for Compas GUI
mongodb://root:M0ngo100500@localhost:27017/
```


#### Docker backup volumes

```bash
# Бэкап данных базы Mongo из именованного тома Windows OC
# где --volumes-from mongo (mongo)
# путь, куда сохранять наши бэкапы -v %cd%:/backup
# ubuntu tar cvf ./backup/mongo.tar /data/db архивация данных из монго и сохранение архива по пути ./backup/mongo.tar
# %cd% для абсолютного пути на Windows а для Linux заменить на $PWD 
docker run --rm --volumes-from mongo -v %cd%:/backup ubuntu tar cvf ./backup/mongo.tar /data/db

#################
# Mongo DB
#################

# Восстановление базы MongoDB из бэкапа архива

# Содание архива данных из MongoDB
docker run --rm --volumes-from mongo -v %cd%:/backup bash -c "cd /data/db && tar xvf /backup/mongo.tar"

# Восстановление данных из MongoDB
docker run --rm --volumes-from mongo -v %cd%:/backup bash -c "rm -rf /data/db/* && tar xvf /backup/mongo.tar"

# Создание бэкапа через строку, не заходя в контейнер
docker exec mongo bash -c "mongodump --db=dev --username=root --password=M0ngo100500 --out=/tmp/backup/${1:-`date '+%Y-%d-%m__%H-%M-%S'`} --authenticationDatabase=admin"

# Восстановление бэкапа через строку, не заходя в контейнер
docker exec mongo bash -c "mongorestore --username=root --password=M0ngo100500 --authenticationDatabase=admin /tmp/backup/2024-26-07__20-47-14"


#################
# PostgreSQL
#################

# Бэкап БД постгреса. Создает архив тома
docker run --rm --volumes-from db_fastapi_2024 -v %cd%:/backup ubuntu tar cvf ./backup/db.tar /var/lib/postgresql/data

# don't work
docker run --rm --volumes-from db_fastapi_2024 -v %cd%:/backup bash -c "rm -rf /var/lib/postgresql/data* && tar xvf /backup/db1.tar"

# backup PostgreSql create
pg_dumpall -c -U postgres > dump_`date +%Y-%m-%d"_"%H_%M_%S`.sql

# backup PostgreSql restore
cat your_dump.sql | psql -U postgres

# бэкап PostgreSQL через утилиту pg_dump (делаем бэкап)
pg_dump -U postgres -Fc > ./tmp/backup/db_sql.dump

# Восстановление базы PostgreSQL утилиту pg_dump (restore)
pg_restore -U postgres -d postgres ./tmp/backup/db_sql.dump

# Бэкап базы одной командой
# где db_fastapi_2024 контейнер
docker exec db_fastapi_2024  bash -c "pg_dump -U postgres -Fc > ./tmp/backup/${1:-`date '+%Y-%d-%m__%H-%M-%S'`}_backup_sql.dump"

# Восстановление через pg_restore не заходя в контейнер
docker exec db_fastapi_2024  bash -c "pg_restore -U postgres -d postgres ./tmp/backup/2024-26-07__17-32-50_backup_sql.dump"
```
