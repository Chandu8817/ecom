from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business = models.CharField(max_length=150)

    def __str__(self):
        return self.business
