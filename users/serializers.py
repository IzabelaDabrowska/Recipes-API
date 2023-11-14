from typing import Dict

from rest_framework.serializers import (CharField, EmailField,
                                        HyperlinkedModelSerializer,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField, Serializer,
                                        SerializerMethodField)

from recipes.models import Recipe
from recipes.serializers import ListRecipeSerializer

from .models import AppUser


class AddRecipeToFavoriteSerializer(Serializer):
    recipe = PrimaryKeyRelatedField(queryset=Recipe.objects.all())


class AppUserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = AppUser
        fields = ["id", "email", "first_name", "last_name"]


class CurrentUserSerializer(ModelSerializer):
    recipes = SerializerMethodField()
    favorites_recipes = ListRecipeSerializer(many=True)

    def get_recipes(self, obj):
        recipes = list(Recipe.objects.filter(author=obj))
        serializer = ListRecipeSerializer(recipes, many=True)
        return serializer.data

    class Meta:
        model = AppUser
        fields = ["id", "first_name", "last_name", "favorites_recipes", "recipes"]


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
