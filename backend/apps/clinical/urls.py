from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.urls import GlobalPlaceholderViewSet

router = DefaultRouter()
router.register('clinical', GlobalPlaceholderViewSet, basename='medicine')

urlpatterns = [
    path('', include(router.urls)),
]