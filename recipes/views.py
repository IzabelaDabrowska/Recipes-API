from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from .models import Recipe
from .permissions import HasObjectPermission
from .serializers import (CreateRecipeSerializer, DetailsRecipeSerializer,
                          ListRecipeSerializer)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasObjectPermission]

    def get_serializer_class(self):
        if self.action == 'list':
            return ListRecipeSerializer
        if self.action == 'retrieve':
            return DetailsRecipeSerializer
        return CreateRecipeSerializer
