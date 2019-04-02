from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    data_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    dist = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    paypal_acc = models.CharField(max_length=1024, null=True, blank=True)
    banck_acc = models.CharField(max_length=1024, null=True, blank=True)

    # related to sponsor attributes
    business = models.CharField(max_length=1024, null=True, blank=True)
    commercial_register_number = models.CharField(max_length=2048, null=True, blank=True)
    logo = models.ImageField(blank=True, null=True, upload_to='uploads/')


    USER_TYPES = (
        ('team_leader', 'Team Leader'),
        ('player', 'Player'),
        ('sponsor', 'Sponsor'),
        ('landlord', 'Land Lord'),
    )


    user_type = models.CharField(max_length=25, choices=USER_TYPES)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"



