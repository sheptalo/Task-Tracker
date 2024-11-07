from django.contrib import admin
from .models import (
    UserModel,
    Role,
    Project,
    Task,
    TaskComment,
    TaskPriority,
    TaskStatus,
    UserProjectAssignment,
)


# Register your models here.
admin.site.register(UserModel)
admin.site.register(Role)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TaskStatus)
admin.site.register(TaskComment)
admin.site.register(TaskPriority)
admin.site.register(UserProjectAssignment)
