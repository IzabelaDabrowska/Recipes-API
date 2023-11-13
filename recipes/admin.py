from django.contrib import admin

from .models import Recipe, RecipeIngredient, RecipeReview, RecipeStep


class RecipeAdmin(admin.ModelAdmin):
    list_display = ["title", 'category', "author", "created_at"]


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ["ingredient", "amount", 'unit']


class RecipeReviewAdmin(admin.ModelAdmin):
    list_display = ["recipe", "review"]


class RecipeStepAdmin(admin.ModelAdmin):
    list_display = ["recipe", "order"]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(RecipeReview, RecipeReviewAdmin)
admin.site.register(RecipeStep, RecipeStepAdmin)
