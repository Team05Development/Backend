### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Team05Development/Backend.git
```

```
cd Backend
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```
Создать суперпользователя:

```
python manage.py createsuperuser
```

Загрузить из фикстур списки с базу данных:

```
python manage.py loaddata events-lists.json
```

Запустить проект:

```
python manage.py runserver
```