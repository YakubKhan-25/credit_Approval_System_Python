from django.db import models

class Loan(models.Model):
    customer = models.ForeignKey('core.Customer', on_delete=models.CASCADE, related_name='loans')
    loan_amount = models.FloatField()
    interest_rate = models.FloatField()
    tenure = models.IntegerField()
    monthly_installment = models.FloatField()
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    emis_paid_on_time = models.IntegerField(default=0)

    def __str__(self):
        return f"Loan {self.id} for {self.customer}"
