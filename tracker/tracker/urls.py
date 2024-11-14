from django.urls import path, include
from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenVerifyView
from django.contrib import admin
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Task Tracker",
        default_version="v1",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="shept@sinortax.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)

urlpatterns = [
    path(
        "docs/",
        schema_view.with_ui(),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path(
        "api/v1/token/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/v1/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"
    ),
    path("api/v1/", include("main.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
