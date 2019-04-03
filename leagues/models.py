from django.db import models
from core.models import User
from teams.models import Team

class League(models.Model):
    name = models.CharField(max_length=255)
    starts_at = models.DateTimeField(null=True, blank=True)
    sponser = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Round(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    teams = models.ManyToManyField(Team, related_name='rounds')
    max_teams = models.PositiveSmallIntegerField(blank=True)


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
    home = models.ForeignKey(Team, related_name='home_matches', blank=True, null=True)
    home_score = models.PositiveSmallIntegerField(blank=True)
    play_by = models.DateTimeField()
    date = models.DateTimeField(blank=True)
    result = models.CharField(max_length=1, default='4', choices=RESULT_CHOICES)

    class Meta:
        unique_together = ('away', 'home')

    def __str__(self):
        return f"Match {self.away.name} vs {self.home.name}"







