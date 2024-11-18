from rest_framework import serializers

from .models import (
    Project,
    Task,
    UserModel,
    TaskComment,
    UserProjectAssignment,
    TaskStatus,
    TaskPriority,
    Role,
    ProjectsHistory,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            "id",
            "avatar",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "projects",
        ]


class RegSerializer(serializers.ModelSerializer):
    # для регистрации
    password = serializers.CharField(min_length=8)

    class Meta:
        model = UserModel
        fields = ["username", "password"]

    def save(self, **kwargs):
        user = UserModel()
        user.username = self.validated_data["username"]
        user.set_password(self.validated_data["password"])
        user.save()
        return user


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = "__all__"


class UserProjectAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProjectAssignment
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name"]


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = ["id", "name"]


class TaskPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPriority
        fields = ["id", "name"]


class ProjectHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsHistory
        fields = "__all__"
