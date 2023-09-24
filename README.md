Система для управления библиотекой видеоконтента cinova (фильмы, сериалы)

Этот проект представляет собой веб-приложение на Django для управления библиотекой фильмов и сериалов.

_______________________________________________________________________________________________________________________________________________________________

Функциональности

● Регистрация и Аутентификация:

Пользователи могут регистрироваться и аутентифицироваться в системе.


● Профили Пользователей:

Пользователи имеют свои профили с возможностью редактирования и загрузки аватаров.

● Добавление и Редактирование Фильмов и Сериалов:

Администраторы могут добавлять и редактировать информацию о фильмах и сериалах, включая название, год выпуска, рейтинг и т.д.

● Система Рецензий и Оценок:

Пользователи могут оставлять рецензии, оценивать фильмы и сериалы.

● Создание и Управление Списками:

Пользователи могут создавать собственные списки (например, "Избранное", "Просмотреть позже").

● Мультиязычность:

Поддержка различных языков интерфейса для удобства пользователей.

● Рекомендации и Персонализированный Контент:

Предложение фильмов на основе истории просмотров и предпочтений пользователей.

● Система Уведомлений:

Уведомления о новых рецензиях, оценках и рекомендациях.


_______________________________________________________________________________________________________________________________________________________________

Инструкции по Развёртыванию

● Установка зависимостей:

pip install -r requirements.txt

● Создание миграций и применение:

python manage.py makemigrations
python manage.py migrate

● Создание суперпользователя (для административной панели):

python manage.py createsuperuser

● Запуск сервера:

python manage.py runserver

● Административная панель:

Перейдите по адресу http://localhost:8000/admin и войдите с использованием учетных данных суперпользователя.

● Добавление Фильмов и Сериалов:

В административной панели можно добавлять и редактировать информацию о фильмах и сериалах.

● Документация API Кинопоиска (опционально):

Документация API Кинопоиска

_______________________________________________________________________________________________________________________________________________________________
