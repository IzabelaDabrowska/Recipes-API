from rest_framework.serializers import ModelSerializer

from ingredients.models import Ingredient


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["name", "id"]
