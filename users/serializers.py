from rest_framework.serializers import HyperlinkedModelSerializer

from .models import AppUser


class AppUserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = AppUser
        fields = ["id", "email", "first_name", "last_name", "is_superuser"]
