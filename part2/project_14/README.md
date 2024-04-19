# Домашнє завдання #14

<h3>Опис:</h3>

<b> html сторінка документація створена за допомогою Sphinx і лежить в теці: </b>

    docs/_build/html/index.html

<b> Запуск контроля пакету pytest-cov: </b>

    pytest --cov=./src --cov-report html tests/

<b> Всі тести знаходяться в теці: </b>

    tests/

<b> Запуск баз даний Postgres та Redis через Docker Compose: </b>

    docker-compose up -d

<b> Запуск веб-сервера Uvicorn командою з директорії main.py: </b>

    py main.py







