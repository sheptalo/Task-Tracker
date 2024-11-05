# Task tracker

## запуск проекта

### Подготовка

1. Необходимо иметь бд postgresql

### Запускаем

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

```bash
cd tracker
```

**_Так как возможно ваша база данных не готова к проекту необходимо выполнить некоторые действия_**

```bash
python manage.py makemigrations
python manage.py migrate
```

и запускаем проект

```bash
python manage.py runserver
```


