from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets, response

from api.v1.serializers.user_serializer import CustomUserSerializer, BalanceSerializer
from users.models import Balance

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "head", "options"]
    permission_classes = (permissions.IsAdminUser,)


class BalanceViewSet(viewsets.ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = (permissions.IsAdminUser,)

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return response.Response({"detail": "Недостаточно прав."}, status=403)
        return super().update(request, *args, **kwargs)