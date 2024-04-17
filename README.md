# API for Funtech - website of IT events
* Available at [Yandex cloud server](http://158.160.154.62/api/events/)
* and also at [funtech.work.gd](http://funtech.work.gd/api/events/).
* [API documentation](http://158.160.154.62/api/schema/redoc/).

Authors:
* Anastasia Grechkina (Github beluza-n, telegram @beluza_n)

## Desicription
Created during Hackaton+ Funtech at Yandex Practicum. Uses Django Rest Framework. Uses PostgreSQL as database.
The project collects IT events. User can register, send application to events, add events to favorites.
Administration through django admin panel. Admin can manage events, accept application of users.

## Stack:
* Python
* Django Rest Framework
* djoser
* PostgreSQL

### How to run the project:
Clone repository and go to it with the terminal::

```
git clone git@github.com:Team05Development/Backend.git
```

```
cd Backend
```

Create and activate virtual environment:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Update pip (optional):

```
python -m pip install --upgrade pip
```

Install dependencies from the requirements.txt:

```
pip install -r requirements.txt
```

Run migrations:

```
python manage.py migrate
```

Launch the Django project:

```
python manage.py runserver
```

### API documentation
You can find request and response examples in the API documentation.
Download yaml-file:

```
/api/schema/
```

Swagger documentation:

```
/api/schema/swagger-ui/
```

Redoc documentation:

```
/api/schema/redoc/
```
