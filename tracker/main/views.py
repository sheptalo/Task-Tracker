import logging

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from dotenv import load_dotenv

from .serializers import (
    UserSerializer,
    ProjectSerializer,
    CommentSerializer,
    UserProjectAssignmentSerializer,
    RoleSerializer,
    TaskSerializer,
    TaskStatusSerializer,
    TaskPrioritySerializer,
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
from .utils import (
    send_websocket,
    filter_get_params,
    order_query,
    send_email,
    date_filter,
)
from tracker import docs

load_dotenv()


@api_view(["GET", "POST"])
def users_view(request):
    if request.method == "GET":
        query = UserModel.objects.all()
        query = order_query(query, request.GET.get("order", ""))
        return Response(UserSerializer(query, many=True).data)
    elif request.method == "POST":
        serializer = update_item(UserSerializer, request.data)
        return Response(serializer.data, status=201)


@api_view(["GET", "PATCH", "DELETE"])
def users_view_item(request, pk: int):
    user = get_object_or_404(UserModel, id=pk)
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)
    elif request.method == "PATCH":
        serializer = update_item(UserSerializer, request.data, user)
        return Response(serializer.data, status=200)
    elif request.method == "DELETE":
        user.delete()
        return Response(
            {"detail": "successfully deleted"},
            status=204,
        )


@swagger_auto_schema(operation_description=docs.projects_get, method="get")
@api_view(["GET", "POST"])
def projects_view(request):
    if request.method == "GET":
        query = Project.objects.all()
        query = order_query(query, request.GET.get("order", ""))
        query = date_filter(
            request.GET.get("mode", "created_at"),
            query,
            request.GET.get("start_date", ""),
            request.GET.get("end_date", ""),
        )
        return Response(ProjectSerializer(query, many=True).data)
    elif request.method == "POST":
        serializer = update_item(ProjectSerializer, request.data)
        return Response(serializer.data, status=201)


@api_view(["GET", "PATCH", "DELETE"])
def projects_view_item(request, pk: int):
    project = get_object_or_404(Project, id=pk)
    if request.method == "GET":
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = update_item(ProjectSerializer, request.data, project)
        return Response(serializer.data, status=200)
    elif request.method == "DELETE":
        project.delete()
        return Response(
            {"detail": "successfully deleted"},
            status=204,
        )


class TasksViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    @swagger_auto_schema(operation_description=docs.tasks_get)
    def list(self, request, *args, **kwargs):
        query = self.queryset
        query = filter_get_params(
            ["status", "priority", "assignee", "tester", "order", "project"],
            query,
            request.GET,
        )

        serializer = TaskSerializer(query, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        a = super().update(request, *args, **kwargs)

        if st := request.data.get("assignee", ""):
            send_websocket(st, "Вы были назначены исполнителем в задаче")
        if request.data.get("status", ""):
            assignee = Task.objects.get(id=kwargs.get("pk")).assignee
            send_websocket(
                assignee, "Статус задачи изменился, проверьте"
            )  # TODO Реализовать ссылку на задачу которая изменилась
        return a


@swagger_auto_schema(operation_description=docs.roles_get, method="get")
@swagger_auto_schema(
    operation_description=docs.roles_post,
    method="post",
    request_body=UserSerializer,
)
@api_view(["GET", "POST"])
def user_roles(request):
    if request.method == "GET":
        serializer = RoleSerializer(Role.objects.all(), many=True)
        return Response(serializer.data, status=200)
    elif request.method == "POST":
        serializer = update_item(RoleSerializer, request.data)
        return Response(serializer.data, status=201)


@api_view(["GET", "PATCH", "DELETE"])
def user_roles_item(request, pk: int):
    role = get_object_or_404(Role, id=pk)
    if request.method == "GET":
        serializer = RoleSerializer(role)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = update_item(RoleSerializer, request.data, role)
        return Response(serializer.data, status=200)
    elif request.method == "DELETE":
        role.delete()
        return Response(
            {"detail": "successfully deleted"},
            status=204,
        )


@swagger_auto_schema(
    operation_description=docs.comments_post,
    method="post",
    query_serializer=CommentSerializer(),
)
@swagger_auto_schema(operation_description=docs.comments_get, method="get")
@api_view(["GET", "POST"])
def comments_view(request):
    priority = TaskComment.objects.all()
    if request.method == "GET":
        priority = filter_get_params(["task"], priority, request.GET)
        serializer = CommentSerializer(priority, many=True)
        return Response(serializer.data, status=200)
    elif request.method == "POST":
        serializer = update_item(CommentSerializer, request.data)
        if st := Task.objects.get(id=request.data["task"]).assignee:
            send_websocket(
                st.id,
                "На вашу задачу добавлен новый коментарий",
            )
        return Response(serializer.data, status=201)


@api_view(["GET", "PATCH", "DELETE"])
def comments_view_item(request, pk: int):
    comment = get_object_or_404(TaskComment, id=pk)
    if request.method == "GET":
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = update_item(CommentSerializer, request.data, comment)
        return Response(serializer.data, status=200)
    elif request.method == "DELETE":
        comment.delete()
        return Response(
            {"detail": "successfully deleted"},
            status=204,
        )


@swagger_auto_schema(
    operation_description=docs.user_project_assignment_post, method="post"
)
@api_view(["GET", "POST"])
def user_project_assignment(request):
    upa = UserProjectAssignment.objects.all()
    if request.method == "GET":
        serializer = UserProjectAssignmentSerializer(upa, many=True)
        return Response(serializer.data, status=200)
    elif request.method == "POST":
        serializer = update_item(UserProjectAssignmentSerializer, request.data)
        project = Project.objects.get(id=request.data.get("project", 0))
        role = Role.objects.get(id=request.data.get("role", 0)).name

        message = (
            f"you assigned to project: {project.title} as {role}. "
            f"Go on site to check more.\n\n\n\n".encode("utf-8")
        )
        send_email(
            UserModel.objects.get(id=request.data.get("user", 0)).email,
            message,
        )

        send_websocket(
            request.data.get("user", 0),
            f"Вы назначены в новый проект {project.title}",
        )
        return Response(serializer.data, status=201)


@api_view(["GET", "PATCH", "DELETE"])
def user_project_assignment_item(request, pk: int):
    upa = get_object_or_404(UserProjectAssignment, id=pk)
    if request.method == "GET":
        serializer = UserProjectAssignmentSerializer(upa)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = update_item(
            UserProjectAssignmentSerializer, request.data, upa
        )
        return Response(serializer.data, status=200)
    elif request.method == "DELETE":
        upa.delete()
        return Response(
            {"detail": "successfully deleted"},
            status=204,
        )


@swagger_auto_schema(
    operation_description=docs.task_priority_get, method="get"
)
@swagger_auto_schema(
    operation_description=docs.task_priority_post,
    method="post",
    query_serializer=TaskPrioritySerializer(),
)
@api_view(["GET", "POST"])
def task_priority(request):
    priority = TaskPriority.objects.all()
    if request.method == "GET":
        serializer = TaskPrioritySerializer(priority, many=True)
        return Response(serializer.data, status=200)
    elif request.method == "POST":
        serializer = update_item(TaskPrioritySerializer, request.data)
        return Response(serializer.data, status=201)


@api_view(["GET", "PATCH", "DELETE"])
def task_priority_item(request, pk: int):
    task = get_object_or_404(TaskPriority, id=pk)
    if request.method == "GET":
        serializer = TaskPrioritySerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = update_item(TaskPrioritySerializer, request.data, task)
        return Response(serializer.data, status=200)
    elif request.method == "DELETE":
        task.delete()
        return Response(
            {"detail": "successfully deleted"},
            status=204,
        )


@swagger_auto_schema(operation_description=docs.task_status_get, method="get")
@swagger_auto_schema(
    operation_description=docs.task_status_post,
    method="post",
    query_serializer=TaskStatusSerializer(),
)
@api_view(["GET", "POST"])
def task_status(request):
    task = TaskStatus.objects.all()
    if request.method == "GET":
        serializer = TaskStatusSerializer(task, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = update_item(TaskStatusSerializer, request.data)
        return Response(serializer.data, status=201)


@api_view(["GET", "PATCH", "DELETE"])
def task_status_item(request, pk: int):
    task = get_object_or_404(TaskStatus, id=pk)
    if request.method == "GET":
        serializer = TaskStatusSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = update_item(TaskStatusSerializer, request.data, task)
        return Response(serializer.data, status=200)
    elif request.method == "DELETE":
        task.delete()
        return Response(
            {"detail": "successfully deleted"},
            status=204,
        )


@swagger_auto_schema(
    operation_description=docs.register_user_post,
    method="post",
    request_body=UserSerializer,
)
@api_view(["POST"])
def register_user(request):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserModel.objects.create_user(
            username=request.data.get("username"),
            password=request.data.get("password"),
        )
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def update_item(serializer, data, obj=None):
    serializer = serializer(obj, data=data, partial=obj is not None)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    if obj is None:
        logging.info(
            f"Создание данных {serializer} со следующими данными {data}"
        )
    else:
        logging.info(f"Обновление данных {obj}, со следующими данными {data}")
    return serializer
