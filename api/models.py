from django.db import models
import datetime

# Create your models here.
class Account(models.Model):
    account_no = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    email = models.CharField(max_length=100, null=False, blank=False)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=200, null=False, blank=False)
    image_path = models.CharField(max_length=500, null=True, blank=True)
    date_registered = models.DateField(default=datetime.date.today)
    date_approved = models.DateField(null=True, blank=True)
    account_type = models.CharField(max_length=10, null=False, blank=False, default='member')
    account_status = models.CharField(max_length=10, null=False, blank=False, default='pending')

    def __str__(self):
        return self.email

class WithdrawalSlip(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_requested = models.DateField(default=datetime.date.today)
    total_amount = models.CharField(max_length=500, null=False, blank=False)
    image_path_passed = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=10, null=False, blank=False, default='pending')
    date_approved = models.DateField(null=True, blank=True)


    def __str__(self):
        return self.status

class DepositSlip(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_requested = models.DateField(default=datetime.date.today)
    total_amount = models.CharField(max_length=500, null=False, blank=False)
    image_path_passed = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=10, null=False, blank=False, default='pending')
    date_approved = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.status

class TransactionRequest(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    request_remarks = models.TextField(null=True, blank=True)
    date_requested = models.DateField(default=datetime.date.today)