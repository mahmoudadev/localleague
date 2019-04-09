from django.db import models
from core.models import Player


class Team(models.Model):
    name = models.CharField(max_length=1024)
    logo = models.ImageField(upload_to='uploads/')
    leader = models.OneToOneField(Player, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player, related_name='teams_as_player')

    def __str__(self):
        return self.name


class PlayerInvite(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)

class TeamRequest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)
