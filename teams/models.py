from django.db import models
from core.models import User


class Team(models.Model):
    name = models.CharField(max_length=1024)
    logo = models.ImageField(upload_to='uploads/teams/logos')
    leader = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teams_as_leader')
    players = models.ForeignKey(User, on_delete=models.CASCADE)



    def __str__(self):
        return self.name
