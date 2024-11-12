# Task tracker

---

## Описание

Task tracker - Упрощенная система управления задачами, которая позволит пользователям создавать и управлять проектами и задачами, назначать исполнителей и отслеживать статус их выполнения.

**Сроки: 5.11.2024-25.11.2024**

---

## Запуск проекта

### Подготовка

1. Необходимо иметь настроенную базу данных postgres, и корне проекта создать файл .env со следующим содержимым

```text
GOOGLE_KEY=Секретный ключ к гугл аккаунту для приложений
SENDER_EMAIL=Гугл почта с которой будут отправляться сообщения
SECRET_KEY='django-insecure-=x%a6c9eiwa@jz2ef$ovxm$08l$p#+9$$zny&46j^!8(d6kk0t'
DB_NAME=Имя базы данных
DB_USER=Имя пользователя имеющего доступ к ней
DB_PASSWORD=Пароль к пользователю
DB_HOST=ip адрес базы данных
```

---

### Запуск

```bash
$ python -m venv venv
```

```bash
$ venv\Scripts\activate
```

```bash
$ pip install -r requirements.txt
```

```bash
$ cd tracker
```

**_Так как возможно ваша база данных не готова к проекту необходимо выполнить некоторые действия_**

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

Запускаем проект

```bash
$ python manage.py runserver
```

---
