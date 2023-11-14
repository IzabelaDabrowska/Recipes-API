from django_filters.rest_framework import CharFilter, FilterSet

from .models import Recipe


class RecipeFilters(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
    ingredient = CharFilter(method='filter_by_ingredient')

    def filter_by_ingredient(self, queryset, name, value):
        return queryset.filter(ingredients__ingredient__icontains=value)

    class Meta:
        model = Recipe
        fields = ["category", "tags"]
