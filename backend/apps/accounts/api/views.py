from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status,generics

from rest_framework.decorators import action

from ..models import User
from .serializers import UserSerializer, ProfileSerializer

class UserViewSet(viewsets.ViewSet,generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['current_user', 'my_profile']:
            return [permissions.IsAuthenticated()]

        return [permissions.IsAdminUser()]

    @action(methods=['get', 'patch'], url_path='profile', detail=False)
    def current_user(self, request):
        u = request.user

        if request.method == 'GET':
            s = UserSerializer(u)
            return Response(s.data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            s = UserSerializer(u, data=request.data, partial=True)
            s.is_valid(raise_exception=True)
            s.save()

            return Response(s.data, status=status.HTTP_200_OK)