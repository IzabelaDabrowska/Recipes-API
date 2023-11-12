from django.contrib import admin

from .models import Recipe, RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ["title", 'category', "author", "created_at"]


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ["ingredient", "amount", 'unit']


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
