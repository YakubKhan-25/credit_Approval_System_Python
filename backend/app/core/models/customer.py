from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    monthly_income = models.IntegerField()
    phone_number = models.BigIntegerField(unique=True)
    approved_limit = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"