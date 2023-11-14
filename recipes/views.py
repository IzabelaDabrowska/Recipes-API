from django.db import transaction
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recipes.filters import RecipeFilters
from tags.models import Tag

from .models import Recipe, RecipeIngredient, RecipeReview, RecipeStep
from .permissions import HasObjectPermission
from .serializers import (CreateRecipeReviewSerializer, CreateRecipeSerializer,
                          DetailsRecipeSerializer, ListRecipeReviewSerializer,
                          ListRecipeSerializer)


class RecipeReviewView(ModelViewSet):
    queryset = RecipeReview.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasObjectPermission]

    def get_queryset(self):
        recipe_id = self.kwargs["recipe_id"]
        return RecipeReview.objects.filter(recipe_id=recipe_id)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ListRecipeReviewSerializer
        return CreateRecipeReviewSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasObjectPermission]
    filterset_class = RecipeFilters

    def get_serializer_class(self):
        if self.action == "list":
            return ListRecipeSerializer
        if self.action == "retrieve":
            return DetailsRecipeSerializer
        return CreateRecipeSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            new_tags = [
                Tag.objects.create(name=t) for t in serializer.validated_data["newTags"]
            ]
            all_tags = new_tags + serializer.validated_data["tags"]
            recipe = Recipe.objects.create(
                title=serializer.validated_data["title"],
                category=serializer.validated_data["category"],
                difficulty_level=serializer.validated_data["difficulty_level"],
                execution_time=serializer.validated_data["execution_time"],
                author=serializer.validated_data["author"],
                image=serializer.validated_data["image"],
            )
            recipe.tags.set(all_tags)
            for i in serializer.validated_data["ingredients"]:
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=i["ingredient"],
                    amount=i["amount"],
                    unit=i["unit"],
                )
            for e in serializer.validated_data["steps"]:
                RecipeStep.objects.create(
                    recipe=recipe,
                    description=e["description"],
                    image=e["image"],
                    order=e["order"],
                )
            response_serializer = DetailsRecipeSerializer(recipe)
        return Response(response_serializer.data, status=201)
