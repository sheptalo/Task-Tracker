from . import views
from django.urls import path

urlpatterns = [
    path(
        "projects/",
        views.Projects.as_view(
            {
                "get": "list",
                "post": "create",
                "update": "update",
            }
        ),
    ),
    path(
        "projects/<int:pk>",
        views.Projects.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "put": "update",
                "delete": "delete",
            }
        ),
    ),
    path("users/", views.Users.as_view({"get": "list", "post": "create"})),
    path("tasks/", views.Tasks.as_view({"get": "list"})),
    path("comments/", views.Comments.as_view({"get": "list"})),
]
