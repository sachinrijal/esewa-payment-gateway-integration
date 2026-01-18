from django.db import models

# Create your models here.

class Donation(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.IntegerField()
    transaction_uuid = models.CharField(max_length=100,blank=True,unique=True)
    status = models.BooleanField(default=False)
    

    def __str__(self):
        return self.name
