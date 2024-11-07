from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"projects", views.ProjectsViewSet)
router.register(r"users", views.UsersViewSet)
router.register(r"user-project-role", views.UserProjectAssignmentViewSet)
router.register(r"roles", views.RolesViewSet)
router.register(r"tasks", views.TasksViewSet)
router.register(r"task-status", views.TaskStatusViewSet)
router.register(r"task-priority", views.TaskPriorityViewSet)
router.register(r"comments", views.CommentsViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", views.RegistrationAPIView.as_view()),
]
