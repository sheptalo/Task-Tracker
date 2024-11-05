from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField


class UserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField("first name", max_length=150, blank=True)
    last_name = models.CharField("last name", max_length=150, blank=True)
    avatar = models.ImageField()
    role = models.CharField(
        max_length=50,
        choices=(("1", "a"), ("2", "b"), ("3", "c")),
    )
    projects = models.CharField(max_length=20)
    history = ArrayField(
        base_field=models.CharField(max_length=50), blank=True, null=True
    )


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=50, choices=(("1", "Активен"), ("2", "Архивирован"))
    )
    participates = ArrayField(
        base_field=models.CharField(max_length=30, null=True),
        blank=True,
        null=True,
    )


class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    worker = models.IntegerField()
    project = models.ForeignKey(Project, models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=(
            ("1", "Grooming"),
            ("2", "In progress"),
            ("3", "Dev"),
            ("4", "Done"),
        ),
    )
    priority = models.CharField(
        max_length=50,
        choices=(("1", "Низкий"), ("2", "Средний"), ("3", "Высокий")),
    )
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField()
    timeline = models.DurationField()
    tester = models.ForeignKey(UserModel, models.DO_NOTHING)


class Comment(models.Model):
    task = models.ForeignKey(Task, models.CASCADE)
    author = models.ForeignKey(UserModel, models.CASCADE)
    message = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now=True)
