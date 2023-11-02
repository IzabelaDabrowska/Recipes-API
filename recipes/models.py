from django.db import models

from categories.models import Category
from tags.models import Tag
from users.models import AppUser

DIFFICULTY_LEVEL = (
    (1, 1),
    (2, 2),
    (3, 3),
)


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    difficulty_level = models.IntegerField(choices=DIFFICULTY_LEVEL, default=1)
    execution_time = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True)
    author = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.title
