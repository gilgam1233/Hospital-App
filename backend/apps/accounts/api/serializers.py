from rest_framework import serializers
from ..models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'phone', 'gender', 'dob', 'province', 'street_address']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)

        user = User.objects.create(**validated_data)

        if profile_data:
            profile_data['img'] = f"https://ui-avatars.com/api/?name={profile_data['full_name']}&background=0D8ABC&color=fff&size=128"
            profile_data['name'] = f"{validated_data['last_name']} {validated_data['first_name']}"
            Profile.objects.create(user=user, **profile_data)

        return user