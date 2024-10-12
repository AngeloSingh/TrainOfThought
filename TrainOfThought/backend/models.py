from django.db import models

class Creator(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length=30)
    description = models.CharField(max_length=150)
    default_reputation = models.FloatField()
    default_hatred = models.FloatField()
    default_likeness = models.FloatField()
    default_popularity = models.FloatField()
    networth = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Bot(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    reputation = models.FloatField()
    hatred = models.FloatField()
    likeness = models.FloatField()
    popularity = models.FloatField()
    networth = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.name


