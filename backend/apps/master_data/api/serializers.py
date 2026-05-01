from rest_framework import serializers
from ..models import Country, Province, District, Ward, Career, EthnicGroup, Specialty, Disease, LabService

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'iso_code']

class ProvinceSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)

    class Meta:
        model = Province
        fields = ['id', 'name', 'code', 'country', 'country_name']

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = '__all__'

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = '__all__'

class EthnicGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = EthnicGroup
        fields = '__all__'

class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'

class LabServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabService
        fields = '__all__'


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['id', 'name', 'description', 'img']