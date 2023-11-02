from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Recipe


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "first_name", "last_name"]


class DetailsRecipeSerializer(ModelSerializer):
    category = SerializerMethodField()
    tags = SerializerMethodField()
    author = AuthorSerializer(read_only=True)

    def get_category(self, obj):
        return obj.category.name

    def get_tags(self, obj):
        return [x.name for x in obj.tags.all()]

    class Meta:
        model = Recipe
        fields = "__all__"


class ListRecipeSerializer(ModelSerializer):
    category = SerializerMethodField()

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Recipe
        fields = ["id", "title", "category", "difficulty_level", "execution_time", "image"]


class CreateRecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"
