from django.db import models
from django.db.models import Q

from core.models import Player

class Team(models.Model):
    name = models.CharField(max_length=1024)
    logo = models.ImageField(upload_to='uploads/')
    leader = models.OneToOneField(Player, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player, related_name='teams_as_player')

    def __str__(self):
        return self.name

    def get_matches(self):
        return self.away_matches.all() | self.home_matches.all()

    def get_points(self):
        points = 0
        for league in self.league_set.all():
            for standing in league.standings_set.filter(team=self):
                points += standing.points

        return points


    def league_wons(self):
        times = 0
        for league in self.league_set.all():
            if self == league.winner:
                times += 1

        return times




class PlayerInvite(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)

class TeamRequest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)
