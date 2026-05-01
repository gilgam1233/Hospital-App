from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

# Import Models và Serializers của bạn
from ..models import (
    Country, Province, District, Ward,
    Career, EthnicGroup, Specialty, Disease, LabService
)
from .serializers import (
    CountrySerializer, ProvinceSerializer, DistrictSerializer, WardSerializer,
    CareerSerializer, EthnicGroupSerializer, SpecialtySerializer, DiseaseSerializer, LabServiceSerializer
)

class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.AllowAny]


class ProvinceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['country']
    search_fields = ['name', 'code']


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['province']


class WardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['district']

class CareerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer
    permission_classes = [permissions.AllowAny]


class EthnicGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EthnicGroup.objects.all()
    serializer_class = EthnicGroupSerializer
    permission_classes = [permissions.AllowAny]


class SpecialtyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name']


class DiseaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'code']


class LabServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LabService.objects.all()
    serializer_class = LabServiceSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name']