import logging
from io import BytesIO

from celery.result import AsyncResult
from django.http import HttpResponse, FileResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
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
    RegSerializer,
    ProjectHistorySerializer,
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
    ProjectsHistory,
)
from .services import generate_project_csv, generate_pdf_file
from .utils import (
    send_websocket,
    filter_get_params,
    order_query,
    send_email,
    date_filter,
)
from . import docs

load_dotenv()


@swagger_auto_schema(
    operation_description=docs.users_get,
    method="get",
    responses={200: openapi.Response("response description", UserSerializer)},
)
@api_view(["GET"])
def users_view(request):
    if request.method == "GET":
        query = UserModel.objects.all()
        query = order_query(query, request.GET.get("order", ""))
        query = filter_get_params(["project"], query, request.GET)
        return Response(UserSerializer(query, many=True).data)


@api_view(["GET", "PATCH", "DELETE"])
def users_view_item(request, pk: int):
    user = get_object_or_404(UserModel, id=pk)
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = update_item(UserSerializer, request.data, user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        user.delete()
        return Response(
            {"detail": "successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


@swagger_auto_schema(
    operation_description=docs.register_user_post,
    method="post",
    request_body=RegSerializer,
)
@api_view(["POST"])
def register_user(request):
    if request.method == "POST":
        serializer = RegSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    operation_description=docs.history_get,
    method="get",
    manual_parameters=[
        openapi.Parameter(
            "user",
            openapi.IN_QUERY,
            description="id пользователя",
            type="int",
        )
    ],
    responses={
        200: openapi.Response("response description", ProjectHistorySerializer)
    },
)
@swagger_auto_schema(
    operation_description=docs.history_post,
    method="post",
    query_serializer=ProjectHistorySerializer(),
)
@api_view(["GET", "POST"])
def history_view(request):
    if request.method == "GET":
        query = ProjectsHistory.objects.all()
        query = filter_get_params(["user"], query, request.GET)
        return Response(ProjectHistorySerializer(query, many=True).data)
    elif request.method == "POST":
        serializer = update_item(ProjectHistorySerializer, request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
def history_view_item(request, pk: int):
    history = get_object_or_404(ProjectsHistory, id=pk)
    if request.method == "GET":
        serializer = ProjectHistorySerializer(history)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = update_item(
            ProjectHistorySerializer, request.data, history
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        history.delete()
        return Response(
            {"detail": "successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


@swagger_auto_schema(
    operation_description=docs.projects_get,
    method="get",
    responses={
        200: openapi.Response("response description", ProjectSerializer)
    },
)
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
def projects_view_item(request, pk: int):
    project = get_object_or_404(Project, id=pk)
    if request.method == "GET":
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = update_item(ProjectSerializer, request.data, project)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        project.delete()
        return Response(
            {"detail": "successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


@swagger_auto_schema(
    operation_description=docs.tasks_get,
    method="get",
    responses={200: openapi.Response("response description", TaskSerializer)},
)
@api_view(["GET", "POST"])
def task_view(request):
    if request.method == "GET":
        query = Task.objects.all()
        query = filter_get_params(
            ["status", "priority", "assignee", "tester", "order", "project"],
            query,
            request.GET,
        )
        query = date_filter(
            request.GET.get("mode", "created_at"),
            query,
            request.GET.get("start_date", ""),
            request.GET.get("end_date", ""),
        )
        serializer = TaskSerializer(query, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = update_item(TaskSerializer, request.data)
        if st := request.data.get("assignee", ""):
            send_websocket(st, "Вам назначена новая задача")

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
def task_view_item(request, pk: int):
    task = get_object_or_404(Task, id=pk)
    if request.method == "GET":
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = update_item(TaskSerializer, request.data, task)
        if st := request.data.get("assignee", ""):
            send_websocket(st, "Вам назначена новая задача")
        if request.data.get("status", ""):
            assignee = Task.objects.get(id=pk).assignee
            send_websocket(assignee, "Статус задачи изменился, проверьте")
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        task.delete()
        return Response(
            {"detail": "successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


@swagger_auto_schema(
    operation_description=docs.roles_get,
    method="get",
    responses={200: openapi.Response("response description", RoleSerializer)},
)
@swagger_auto_schema(
    operation_description=docs.roles_post,
    method="post",
    request_body=UserSerializer,
)
@api_view(["GET", "POST"])
def user_roles(request):
    if request.method == "GET":
        serializer = RoleSerializer(Role.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = update_item(RoleSerializer, request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
def user_roles_item(request, pk: int):
    role = get_object_or_404(Role, id=pk)
    if request.method == "GET":
        serializer = RoleSerializer(role)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = update_item(RoleSerializer, request.data, role)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        role.delete()
        return Response(
            {"detail": "successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


@swagger_auto_schema(
    operation_description=docs.comments_post,
    method="post",
    query_serializer=CommentSerializer(),
)
@swagger_auto_schema(
    operation_description=docs.comments_get,
    method="get",
    responses={
        200: openapi.Response("response description", CommentSerializer)
    },
)
@api_view(["GET", "POST"])
def comments_view(request):
    priority = TaskComment.objects.all()
    if request.method == "GET":
        priority = filter_get_params(["task"], priority, request.GET)
        serializer = CommentSerializer(priority, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = update_item(CommentSerializer, request.data)
        if st := Task.objects.get(id=request.data["task"]).assignee:
            send_websocket(
                st.id,
                "На вашу задачу добавлен новый коментарий",
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
def comments_view_item(request, pk: int):
    comment = get_object_or_404(TaskComment, id=pk)
    if request.method == "GET":
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = update_item(CommentSerializer, request.data, comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        comment.delete()
        return Response(
            {"detail": "successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


@swagger_auto_schema(
    operation_description=docs.user_project_assignment_post, method="post"
)
@swagger_auto_schema(
    operation_description=docs.user_project_assignment_get,
    method="get",
    responses={
        200: openapi.Response(
            "response description", UserProjectAssignmentSerializer
        )
    },
)
@api_view(["GET", "POST"])
def user_project_assignment(request):
    upa = UserProjectAssignment.objects.all()
    if request.method == "GET":
        upa = filter_get_params(["project"], upa, request.GET)
        serializer = UserProjectAssignmentSerializer(upa, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        upa.delete()
        return Response(
            {"detail": "successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


@swagger_auto_schema(
    operation_description=docs.task_priority_get,
    method="get",
    responses={
        200: openapi.Response("response description", TaskPrioritySerializer)
    },
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
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = update_item(TaskPrioritySerializer, request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
def task_priority_item(request, pk: int):
    task = get_object_or_404(TaskPriority, id=pk)
    if request.method == "GET":
        serializer = TaskPrioritySerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = update_item(TaskPrioritySerializer, request.data, task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        task.delete()
        return Response(
            {"detail": "successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


@swagger_auto_schema(
    operation_description=docs.task_status_get,
    method="get",
    responses={
        200: openapi.Response("response description", TaskStatusSerializer)
    },
)
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
def task_status_item(request, pk: int):
    task = get_object_or_404(TaskStatus, id=pk)
    if request.method == "GET":
        serializer = TaskStatusSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = update_item(TaskStatusSerializer, request.data, task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        task.delete()
        return Response(
            {"detail": "successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


@swagger_auto_schema(operation_description=docs.export, method="get")
@api_view(["GET"])
def export(request):
    project_id = request.GET.get("project_id", 1)
    if not project_id:
        return Response(
            {
                "detail": "Укажите в query параметрах id проекта пример: ?project_id=1"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    project = get_object_or_404(Project, id=project_id)
    formatter = request.GET.get("formatter", "pdf")
    if formatter == "csv":
        res = generate_project_csv.delay(project.id)
        result = AsyncResult(res.id)
        data = result.get()
        response = HttpResponse(data, content_type='text/csv')
        response[
            'Content-Disposition'] = f'attachment; filename="{project.title}.csv"'
        return response
    elif formatter == "pdf":
        file = generate_pdf_file.delay(project.id, project.title)
        filepath = file.get()

        with open(filepath, "rb") as f:
            response = FileResponse(
                BytesIO(bytes(f.read())),
                as_attachment=True,
                filename=f"{project.title}.pdf",
            )
            f.close()
        return response
    return Response(
        {"detail": "Не поддерживаемый formatter, используйте pdf или csv"},
        status=status.HTTP_400_BAD_REQUEST,
    )


def update_item(serializer, data, obj=None):
    serializer = serializer(obj, data=data, partial=obj is not None)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    if obj is None:
        logging.info(
            f"Создание данных {serializer} со следующими данными {data}"
        )
    else:
        logging.info(
            f"Обновление данных {obj.__class__.__name__, obj.id}, "
            f"со следующими данными {data}"
        )
    return serializer
