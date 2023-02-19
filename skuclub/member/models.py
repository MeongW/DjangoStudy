from django.db import models
class Account(models.Model):
    account_email = models.CharField(max_length=64, unique=True)
    account_pw = models.CharField(max_length=32)
    account_name = models.CharField(max_length=32)
    account_create_dt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "accounts"
