import base64
import uuid
from statistics import mean

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import (CharField, CurrentUserDefault,
                                        HiddenField, ImageField,
                                        ListSerializer, ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField)

from .models import Recipe, RecipeIngredient, RecipeReview, RecipeStep


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
        file = SimpleUploadedFile(
            name=complete_file_name, content=decoded_file, content_type=mime_type
        )

        return super().to_internal_value(file)


class RecipeIngredientSerializer(ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ["ingredient", "amount", "unit"]


class RecipeStepSerializer(ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = RecipeStep
        fields = ["description", "image", "order"]


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "first_name", "last_name"]


class CreateRecipeReviewSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    def to_internal_value(self, instance):
        representation = super().to_internal_value(instance)
        recipe_id = (
            self.context.get("request").parser_context.get("kwargs").get("recipe_id")
        )
        recipe = get_object_or_404(Recipe.objects.all(), id=recipe_id)
        representation["recipe"] = recipe
        return representation

    class Meta:
        model = RecipeReview
        fields = ["id", "recipe", "review", "description", "user"]
        extra_kwargs = {"recipe": {"read_only": True}}


class ListRecipeReviewSerializer(ModelSerializer):
    user = AuthorSerializer(read_only=True)
    recipe = PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = RecipeReview
        fields = ["id", "recipe", "review", "description", "user"]


class DetailsRecipeSerializer(ModelSerializer):
    category = SerializerMethodField()
    tags = SerializerMethodField()
    average_review = SerializerMethodField()
    ingredients = RecipeIngredientSerializer(read_only=True, many=True)
    steps = RecipeStepSerializer(read_only=True, many=True)
    author = AuthorSerializer(read_only=True)

    def get_category(self, obj):
        return obj.category.name

    def get_tags(self, obj):
        return [x.name for x in obj.tags.all()]

    def get_average_review(self, obj):
        reviews = list(RecipeReview.objects.filter(recipe=obj))
        if reviews:
            return mean([x.review for x in reviews])
        return 0

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "category",
            "tags",
            "difficulty_level",
            "execution_time",
            "created_at",
            "image",
            "author",
            "average_review",
            "ingredients",
            "steps",
        ]


class ListRecipeSerializer(ModelSerializer):
    category = SerializerMethodField()
    average_review = SerializerMethodField()

    def get_category(self, obj):
        return obj.category.name

    def get_average_review(self, obj):
        reviews = list(RecipeReview.objects.filter(recipe=obj))
        if reviews:
            return mean([x.review for x in reviews])
        return 0

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "category",
            "difficulty_level",
            "execution_time",
            "image",
            "average_review",
            "created_at",
        ]


class CreateRecipeSerializer(ModelSerializer):
    image = Base64ImageField()
    newTags = ListSerializer(child=CharField(), default=[])
    ingredients = RecipeIngredientSerializer(many=True)
    steps = RecipeStepSerializer(many=True)
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
            "steps",
        ]
