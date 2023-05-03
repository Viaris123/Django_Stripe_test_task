from django.db import models


class Item(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    prod_id = models.CharField(max_length=255)

    class Meta:
        ordering = ('name', 'price')

    def __str__(self):
        return self.name
