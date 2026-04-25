"""
URL configuration for ecourseapisv1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from apps.accounts.admin.admin_site import hospital_admin_site
from requests import Response

from rest_framework import permissions, viewsets, status
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

class GlobalPlaceholderViewSet(viewsets.ViewSet):
    def list(self, request):
        # Trả về tên app đang gọi để bạn dễ phân biệt khi test
        app_name = request.path.split('/')[2]
        return Response({
            "message": f"API của app [{app_name}] đang được xây dựng.",
            "status": "placeholder"
        }, status=status.HTTP_200_OK)

schema_view = get_schema_view(
    openapi.Info(
        title="Course API",
        default_version='v1',
        description="APIs for CourseApp",
        contact=openapi.Contact(email="thanh.dh@ou.edu.vn"),
        license=openapi.License(name="Dương Hữu Thành@2025"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include('apps.accounts.urls')),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/master-data/', include('apps.master_data.urls')),
    path('api/appointments/', include('apps.appointments.urls')), # <--- NÊN CÓ Ở ĐÂY
    path('api/clinical/', include('apps.clinical.urls')),
    path('api/pharmacy/', include('apps.pharmacy.urls')),
    path('admin/', hospital_admin_site.urls),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^swagger/$',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$',
            schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
    path('o/', include('oauth2_provider.urls',
                       namespace='oauth2_provider'))
]
