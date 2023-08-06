=====
Zibal
=====

A Django app for bank payments by Zibal (https://zibal.ir/)

Detailed documentation is in the "docs" directory.

Quick start
-----------
### 0. install

```sh
pip install requests
pip install zibal-django
```

### 1. start
Add "zibal" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'zibal',
    ]

### 2. migrate
Run ``python manage.py migrate`` to create the zibal models.

### 3. admin
Start the development server and visit http://127.0.0.1:8000/admin/ for Purchase historys Model in admin.

### 4.Instructions
For each transaction you first need to request and then confirm it.
For this operation, you can use 2 methods : request and callback.
You can use the Request method anywhere in the project. For the callback method, it is recommended to write once in a view with a fixed address and always use it.

See the GitHub page of the project for more information https://github.com/mohammad3020/django-zibal