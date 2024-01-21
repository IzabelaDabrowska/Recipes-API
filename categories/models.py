from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name
