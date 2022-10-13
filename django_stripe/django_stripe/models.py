from django.db import models


class Item(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    price_id = models.CharField(max_length=100)
    prod_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name
