from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("users/", views.users_view),
    path("users/<int:pk>/", views.users_view_item),
    path("history/", views.history_view),
    path("history/<int:pk>/", views.history_view_item),
    path("register/", views.register_user),
    path("tasks/", views.task_view),
    path("tasks/<int:pk>/", views.task_view_item),
    path("task-status/", views.task_status),
    path("task-status/<int:pk>/", views.task_status_item),
    path("task-priority/", views.task_priority),
    path("task-priority/<int:pk>/", views.task_priority_item),
    path("roles/", views.user_roles),
    path("roles/<int:pk>/", views.user_roles_item),
    path("projects/", views.projects_view),
    path("projects/<int:pk>/", views.projects_view_item),
    path("comments/", views.comments_view),
    path("comments/<int:pk>/", views.comments_view_item),
    path("user-project-role/", views.user_project_assignment),
    path("user-project-role/<int:pk>/", views.user_project_assignment_item),
    path("export/", views.export),
]
