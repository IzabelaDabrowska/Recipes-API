from django.db import models

from categories.models import Category
from tags.models import Tag
from users.models import AppUser

DIFFICULTY_LEVEL = (
    (1, 1),
    (2, 2),
    (3, 3),
)


REVIEW = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)


GRAM = "gr"
KILOGRAM = "kg"
MILLILITER = "ml"
LITER = "l"
TEASPOON = "tsp"
TABLESPOON = "tbsp"
PIECE = "piece"


UNIT = (
    (GRAM, "gram"),
    (KILOGRAM, "kilogram"),
    (MILLILITER, "milliliter"),
    (LITER, "liter"),
    (TEASPOON, "teaspoon"),
    (TABLESPOON, "tablespoon"),
    (PIECE, "piece"),
)


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    difficulty_level = models.IntegerField(choices=DIFFICULTY_LEVEL, default=1)
    execution_time = models.IntegerField()
    created_at = models.DateField(blank=True, auto_now_add=True)
    image = models.ImageField(blank=True, null=True)
    author = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    ingredient = models.CharField(max_length=20)
    amount = models.IntegerField()
    unit = models.CharField(choices=UNIT, max_length=15, default=GRAM)

    def __str__(self) -> str:
        return self.recipe.title


class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="steps")
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    order = models.IntegerField()

    def __str__(self) -> str:
        return self.recipe.title


class RecipeReview(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    author = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    review = models.IntegerField(choices=REVIEW)
    description = models.CharField(max_length=300)
    created_at = models.DateField(blank=True, auto_now_add=True)

    def __str__(self) -> str:
        return self.recipe.title
