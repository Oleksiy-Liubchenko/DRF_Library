from django.db import models
from model_utils import Choices


class Books(models.Model):
    COVER_CHOICE = Choices(
        ("H", "Hard"),
        ("S", "Soft")
    )

    title = models.TextField(max_length=90)
    author = models.CharField(max_length=60)
    cover = models.CharField(max_length=4, choices=COVER_CHOICE)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title
