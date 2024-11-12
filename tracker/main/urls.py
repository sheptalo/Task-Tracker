from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"user-project-role", views.UserProjectAssignmentViewSet)
router.register(r"tasks", views.TasksViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("users/", views.users_view),
    path("users/<int:pk>/", views.users_view_item),
    path("register/", views.register_user),
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
]
