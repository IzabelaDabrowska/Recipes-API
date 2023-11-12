from typing import Dict

from rest_framework.serializers import (CharField, EmailField,
                                        HyperlinkedModelSerializer,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField, Serializer)

from recipes.models import Recipe

from .models import AppUser


class AddRecipeToFavoriteSerializer(Serializer):
    recipe = PrimaryKeyRelatedField(queryset=Recipe.objects.all())


class AppUserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = AppUser
        fields = ["id", "email", "first_name", "last_name", "is_superuser"]


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = AppUser
        fields = ["email", "first_name", "last_name", "password"]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data: Dict) -> AppUser:
        created_user: AppUser = super().create(validated_data)
        created_user.register(created_user.password)
        return created_user


class ActivateAccountSerializer(Serializer):
    activation_code = CharField(max_length=8)
    email = EmailField()


class ResendActivationCodeSerializer(Serializer):
    email = EmailField()
