from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.master_data.api.views import (
    CountryViewSet, ProvinceViewSet, DistrictViewSet, WardViewSet,
    CareerViewSet, EthnicGroupViewSet, SpecialtyViewSet, DiseaseViewSet, LabServiceViewSet
)

router = DefaultRouter()


router.register('countries', CountryViewSet, basename='country')
router.register('provinces', ProvinceViewSet, basename='province')
router.register('districts', DistrictViewSet, basename='district')
router.register('wards', WardViewSet, basename='ward')

router.register('careers', CareerViewSet, basename='career')
router.register('ethnic-groups', EthnicGroupViewSet, basename='ethnic-group')

router.register('specialties', SpecialtyViewSet, basename='specialty')
router.register('diseases', DiseaseViewSet, basename='disease')
router.register('lab-services', LabServiceViewSet, basename='lab-service')


urlpatterns = [
    path('', include(router.urls)),
]