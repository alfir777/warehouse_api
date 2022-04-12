# warehouse api

Тестовое задание

## Запуск проекта

1. Клонировать репозиторий или форк

```
git clone https://github.com/alfir777/warehouse_api.git
```

2. Выполнить копирование файла .env_template на .env и выставить свои параметры

```
cd warehouse_api/
cp .env_template .env
```

3. Развернуть контейнеры с помощью в docker-compose

```
docker-compose -f docker-compose.yml up -d
```

3. **ИЛИ** Установка зависимостей

```
pip install -r requirements.txt
```

4. Запуск

```
python3 main.py
```

## Запуск тестов

1. Выставить в .env файле TESTING на True
2. Установить зависимости

```
pip install -r requirements_dev.txt
```

3. Запуск

```
pytest -v
```