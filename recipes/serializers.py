import base64
import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import (CharField, CurrentUserDefault,
                                        HiddenField, ImageField,
                                        ListSerializer, ModelSerializer,
                                        SerializerMethodField)

from .models import Recipe, RecipeIngredient


class Base64ImageField(ImageField):
    allowed_mime_types = ("image/jpg", "image/png", "image/jpeg", "image/bmp")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if data in (None, "", [], (), {}):
            return None

        if not isinstance(data, str):
            raise ValidationError(
                message=_(
                    f"Invalid image type. Wanted base64 string, got: {type(data)}"
                )
            )

        if ";base64," not in data:
            raise ValidationError(message=_("Invalid base64"))

        header, base64_data = data.split(";base64,")
        mime_type = header.replace("data:", "")

        if mime_type not in self.allowed_mime_types:
            raise ValidationError(message=_("Invalid file type"))

        decoded_file = base64.b64decode(base64_data)
        file_name = str(uuid.uuid4())
        file_extension = mime_type.replace("image/", "")
        complete_file_name = file_name + "." + file_extension
        file = SimpleUploadedFile(name=complete_file_name, content=decoded_file, content_type=mime_type)

        return super().to_internal_value(file)


class RecipeIngredientSerializer(ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ["ingredient", "amount", "unit"]


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "first_name", "last_name"]


class DetailsRecipeSerializer(ModelSerializer):
    category = SerializerMethodField()
    tags = SerializerMethodField()
    ingredients = RecipeIngredientSerializer(read_only=True, many=True)
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
        fields = [
            "id",
            "title",
            "category",
            "difficulty_level",
            "execution_time",
            "image",
        ]


class CreateRecipeSerializer(ModelSerializer):
    image = Base64ImageField()
    newTags = ListSerializer(child=CharField(), default=[])
    ingredients = RecipeIngredientSerializer(many=True)
    author = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Recipe
        fields = [
            "title",
            "category",
            "difficulty_level",
            "execution_time",
            "image",
            "tags",
            "newTags",
            "ingredients",
            "author",
        ]
