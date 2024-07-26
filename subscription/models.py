from django import db
from django.db import models
from django.conf import settings
# from db_connnection import db  # Import your MongoDB client instance
from django.db import models



class Subscription(models.Model): # its a subscription models to store the data into mongodb 
    user_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    subscription_id = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} - {self.subscription_id}"

    class Meta: # delaring the collection 
        db_table = 'subscription_subscription'

# models.py

from django.db import models
from django.utils import timezone

class DailyPass(models.Model):
    pass_code = models.IntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    company = models.CharField(max_length=20)
    num_people = models.IntegerField(default=1)  # Number of people associated with the pass
    reference_name = models.CharField(max_length=100)  # Reference name for the pass

    def is_valid(self):
        now = timezone.now()
        return self.valid_from <= now <= self.valid_to

    def __str__(self):
        return f"Daily Pass {self.pass_code}"



# ------------------------------------------end of models.py subscription------------------------------------------------------        



# class DailyPass(models.Model):
#     pass_code = models.IntegerField()
#     valid_from = models.DateTimeField()
#     valid_to = models.DateTimeField()
#     company = models.CharField(max_length=20)
#     num_people = models.IntegerField(default=1)  # Number of people associated with the pass
#     reference_name = models.CharField(max_length=100)  # Reference name for the pass

#     def is_valid(self):
#         now = timezone.now()
#         return self.valid_from <= now <= self.valid_to

#     def __str__(self):
#         return f"Daily Pass {self.pass_code}"