import os

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from dotenv import load_dotenv

from .serializers import (
    UserSerializer,
    ProjectSerializer,
    CommentSerializer,
    UserProjectAssignmentSerializer,
    RoleSerializer,
)
from .models import (
    Project,
    Task,
    TaskComment,
    UserModel,
    UserProjectAssignment,
    TaskStatus,
    TaskPriority,
    Role,
)

load_dotenv()


class UsersViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    permission_classes = (IsAuthenticated,)


class ProjectsViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)


class TasksViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated,)


class RolesViewSet(ModelViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    permission_classes = (IsAuthenticated,)


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = TaskComment.objects.all()
    permission_classes = (IsAuthenticated,)


class UserProjectAssignmentViewSet(ModelViewSet):
    serializer_class = UserProjectAssignmentSerializer
    queryset = UserProjectAssignment.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        project = Project.objects.get(id=request.data.get("project", 0)).title
        role = Role.objects.get(id=request.data.get("role", 0)).name
        from smtplib import SMTP

        smtp_obj = SMTP("smtp.gmail.com", 587)
        smtp_obj.starttls()
        smtp_obj.login("solovovartem99", os.environ.get("GOOGLE_KEY"))
        smtp_obj.sendmail(
            "solovovartem99@gmail.com",
            UserModel.objects.get(id=request.data.get("user", 0)).email,
            f"you assigned to project: {project} as {role}. "
            f"Go on site to check more.\n\n\n\n",
        )
        smtp_obj.quit()

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class TaskPriorityViewSet(ModelViewSet):
    serializer_class = TaskPriority
    queryset = TaskPriority.objects.all()
    permission_classes = (IsAuthenticated,)


class TaskStatusViewSet(ModelViewSet):
    serializer_class = TaskStatus
    queryset = TaskStatus.objects.all()
    permission_classes = (IsAuthenticated,)


class RegistrationAPIView(CreateAPIView):
    serializer_class = UserModel
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserModel.objects.create_user(
            username=request.data.get("username"),
            password=request.data.get("password"),
        )
        user.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
