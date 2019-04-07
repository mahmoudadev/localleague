from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.db import models
from sponsorships.models import SponsorshipPackge


class User(AbstractUser):
    photo = models.ImageField(null=True, blank=True, upload_to='uploads/')
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    dist = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    paypal_account = models.CharField(max_length=1024, null=True, blank=True)
    bank_account = models.CharField(max_length=1024, null=True, blank=True)

    USER_TYPES = (
        ('team_leader', 'Team Leader'),
        ('player', 'Player'),
        ('sponsor', 'Sponsor'),
        ('landlord', 'Land Lord'),
    )


    user_type = models.CharField(max_length=25, choices=USER_TYPES)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Player(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    position = models.CharField(max_length=255, null=True, blank=True)
    is_teamleader = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class LandLord(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username


class Sponsor(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    # related to sponsor attributes
    packge = models.ForeignKey(SponsorshipPackge, null=True, blank=True, on_delete=models.CASCADE)
    business = models.CharField(max_length=1024, null=True, blank=True)
    commercial_register_number = models.CharField(max_length=2048, null=True, blank=True)
    logo = models.ImageField(blank=True, null=True, upload_to='uploads/')


    def has_package(self):
        return self.packge


    def __str__(self):
        return self.user.username


def create_user_type_object(sender,instance, created, **kwargs):
    if created:
        if instance.user_type == 'team_leader':
            Player.objects.create(user=instance, is_teamleader=True)
            print("Team Leader Object Created")
        elif instance.user_type == 'player':
            Player.objects.create(user=instance)
            print("Player Object Created")
        elif instance.user_type == 'sponsor':
            Sponsor.objects.create(user=instance)
            print("Sponsor Object Created")
        elif instance.user_type == 'landlord':
            LandLord.objects.create(user=instance)
            print("Landlord Object Created")
        else:
            pass

post_save.connect(create_user_type_object, sender=User)
