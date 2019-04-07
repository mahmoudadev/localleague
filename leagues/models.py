from django.db import models
from core.models import User, Sponsor
from teams.models import Team
from fields.models import Field
from django.db.models.signals import post_save, m2m_changed


class League(models.Model):
    name = models.CharField(max_length=255)
    starts_at = models.DateTimeField(null=True, blank=True)
    teams = models.ManyToManyField(Team)
    fees_per_team = models.FloatField(default=99.0)
    sponsor = models.ForeignKey(Sponsor, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Round(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.league.name} - {self.name}"


class Match(models.Model):
    RESULT_CHOICES = (
        ('1', 'Away Team Wins!'),
        ('2', 'Home Team Wins!'),
        ('3', 'Draw!'),
        ('4', 'Pending'),
    )
    location = models.ForeignKey(Field, null=True, blank=True, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, related_name='matches', on_delete=models.CASCADE)
    away = models.ForeignKey(Team, related_name='away_matches', blank=True, null=True, on_delete=models.CASCADE)
    away_score = models.PositiveSmallIntegerField(blank=True, null=True)
    home = models.ForeignKey(Team, related_name='home_matches', blank=True, null=True, on_delete=models.CASCADE)
    home_score = models.PositiveSmallIntegerField(blank=True, null=True)
    date = models.DateTimeField(null=True, blank=True)
    result = models.CharField(max_length=1, default='4', choices=RESULT_CHOICES)

    class Meta:
        unique_together = ('away', 'home')

    def __str__(self):
        return f"Match {self.away.name} vs {self.home.name}"


class Standings(models.Model):
    league = models.ForeignKey(League, null=True, blank=True, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, null=True, blank=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)

    # standings table info
    games_played = models.IntegerField(verbose_name="Games Played", default=0)

    points = models.IntegerField(verbose_name="Points", default=0)

    wins = models.IntegerField(verbose_name="Wins", default=0)

    draws = models.IntegerField(verbose_name="Draws", default=0)

    losses = models.IntegerField(verbose_name="Losses", default=0)

    def __str__(self):
        return f"{self.league.name} - {self.team.name} - {self.match} Result"


class ParticipateInvite(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.league.name} Invitation"


def send_league_invitation(sender, instance, created, **kwargs):
    print(kwargs)
    print(instance.teams.all())
    print(created)
    sponsor = instance.sponsor
    if not  sponsor.user.participateinvite_set.filter(league=instance, checked=False):
        print('sponsor invite sent')
        ParticipateInvite.objects.create(league=instance, participant=sponsor.user)


def send_to_team_leader(sender, instance, **kwargs):
    teams = instance.teams.all()
    for team in teams:
      if not team.leader.user.participateinvite_set.filter(league=instance, team=team, checked=False):
            print('team invitation sent')
            ParticipateInvite.objects.create(league=instance, team=team, participant=team.leader.user)


post_save.connect(send_league_invitation, sender=League)
m2m_changed.connect(send_to_team_leader, sender=League.teams.through)
