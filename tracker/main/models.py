from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        default="default_avatar.png",
        verbose_name="Аватар",
    )
    role = models.ForeignKey(
        "Role",
        on_delete=models.SET_NULL,
        null=True,
        related_name="users",
        verbose_name="Роль",
    )
    projects = models.ManyToManyField(
        "Project",
        related_name="projects",
        verbose_name="Текущие проекты",
        null=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_choices = (("active", "Активен"), ("archived", "Архивирован"))
    status = models.CharField(
        max_length=10, choices=status_choices, default="active"
    )

    users = models.ManyToManyField(UserModel, through="UserProjectAssignment")

    def __str__(self):
        return self.title


class UserProjectAssignment(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.user.username} ({self.role}) - {self.project}"

    class Meta:
        unique_together = ("user", "project")


class TaskStatus(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class TaskPriority(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    assignee = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assignee",
    )
    status = models.ForeignKey(TaskStatus, on_delete=models.PROTECT)
    priority = models.ForeignKey(TaskPriority, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    tester = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Комментарий к задаче "{self.task}" от {self.author}'
