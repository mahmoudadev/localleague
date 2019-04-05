from django.db import models
from core.models import User
from teams.models import Team
from django.db.models.signals import post_save

class League(models.Model):
    name = models.CharField(max_length=255)
    starts_at = models.DateTimeField(null=True, blank=True)
    sponser = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Round(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


class Match(models.Model):
    RESULT_CHOICES = (
        ('1', 'Away Team Wins!'),
        ('2', 'Home Team Wins!'),
        ('3', 'Draw!'),
        ('4', 'Pending'),
    )

    round = models.ForeignKey(Round, related_name='matches', on_delete=models.CASCADE)
    away = models.ForeignKey(Team, related_name='away_matches', blank=True, null=True, on_delete=models.CASCADE)
    away_score = models.PositiveSmallIntegerField(blank=True)
    home = models.ForeignKey(Team, related_name='home_matches', blank=True, null=True, on_delete=models.CASCADE)
    home_score = models.PositiveSmallIntegerField(blank=True)
    date = models.DateTimeField(null=True, blank=True)
    result = models.CharField(max_length=1, default='4', choices=RESULT_CHOICES)

    class Meta:
        unique_together = ('away', 'home')

    def __str__(self):
        return f"Match {self.away.name} vs {self.home.name}"


class Standings(models.Model):
    league = models.ForeignKey(League, null=True, blank=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)

    # standings table info
    games_played = models.IntegerField(verbose_name="Games Played", default=0)

    points = models.IntegerField(verbose_name="Points", default=0)

    wins = models.IntegerField(verbose_name="Wins", default=0)

    draws = models.IntegerField(verbose_name="Draws", default=0)

    losses = models.IntegerField(verbose_name="Losses", default=0)







