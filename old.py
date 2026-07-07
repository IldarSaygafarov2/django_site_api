# django pillow python-dotenv psycopg2-binary

# №1 - создать проект
# django-admin - дополнительная программа для работы с django
# django-admin startproject название_проекта - создает отдельную папку с проектом
# django-admin startproject название_проекта . - создает проект в той папке
# в которой мы находимся

# №2 - создать приложение
# python manage.py startapp название_приложения

# №3 - запуск локального сервера
# python manage.py runserver

# синтаксис шаблонизатора

# {% название_функции %}
# {% extends 'base.html' %} - наследование от базового шаблона проекта


# TODO: сделать переход на страницу http://127.0.0.1:8000/about/
# {% url 'название_ссылки' получает ссылку по названию %}
# python manage.py migrate - выполняет файлы миграций всех приложений
# python manage.py createsuperuser - команда для создания администратора
