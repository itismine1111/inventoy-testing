from django.db import models

# Create your models here.

class SauceModel(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)



class SandwichModel(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    sauces = models.ManyToManyField(SauceModel)

    class Meta:
        verbose_name_plural = "User Roles"

