from django.db import models
from core.models import User, Sponsor
from teams.models import Team
from fields.models import Field
from django.db.models.signals import post_save, m2m_changed


class League(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    teams = models.ManyToManyField(Team)
    fees_per_team = models.FloatField(default=99.0)
    sponsor = models.ForeignKey(Sponsor, null=True, on_delete=models.CASCADE)
    winner = models.OneToOneField(Team, null=True, blank=True , related_name='league_winner', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def is_finished(self):
        if self.winner:
            return True
        else:
            return False

    def get_landlords(self):
        rounds = self.round_set.all()
        landlords = []
        for round in rounds:
            matches = round.matches.all()
            for match in matches:
                landlords.append({'landlord':match.location.owner,  'match': match})

        return landlords




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

    def match_teams(self):
        return [self.home, self.away]

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

    def __str__(self):
        return f"{self.league.name} - {self.team.name} Result"


class ParticipateInvite(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.league.name} Invitation"


class FieldReseravtion(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True)
    landlord = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.league.name} {self.match} Field Reservation"


def notify_sponsor_or_update_league(sender, instance, created, update_fields, **kwargs):
    print(kwargs)
    print(instance.teams.all())
    print(created)
    if created or 'sponsor' in update_fields:
        sponsor = instance.sponsor
        if sponsor:
            if not  sponsor.user.participateinvite_set.filter(league=instance, checked=False):
                print('sponsor invite sent')
                ParticipateInvite.objects.create(league=instance, participant=sponsor.user)




def notify_team_leader(sender, instance, **kwargs):
    teams = instance.teams.all()
    for team in teams:
        try:

           s =  Standings.objects.get(team=team, league=instance)
           print(s)
           print('standings founded')
        except Exception as e:
            print(str(e))
            s = Standings.objects.create(team=team, league=instance)

        if not team.leader.user.participateinvite_set.filter(league=instance, team=team, checked=False):
                print('team invitation sent')
                ParticipateInvite.objects.create(league=instance, team=team, participant=team.leader.user)



def notify_landlord_or_update_match(sender, instance, created, update_fields, **kwargs):
    print(update_fields)
    # check to send league invitation to landlord
    if instance.location:
        if created or 'location' in update_fields:
            print('hit this line')
            landlord = instance.location.owner
            if not  landlord.user.participateinvite_set.filter(league=instance.round.league, participant=landlord.user, match=instance, checked=False):
                print('landlord invite sent')
                ParticipateInvite.objects.create(league=instance.round.league, match=instance, participant=landlord.user)

    if created or 'result' in update_fields:
        try:
            home_team = Standings.objects.get(team=instance.home, league=instance.round.league)
            away_team = Standings.objects.get(team=instance.away, league=instance.round.league)
        except Exception:
            home_team = Standings.objects.create(team=instance.home, league=instance.round.league)
            away_team = Standings.objects.create(team=instance.away, league=instance.round.league)

        if instance.result == '1':
            home_team.games_played += 1
            away_team.games_played += 1
            away_team.wins += 1
            away_team.points += 3
            home_team.losses += 1
            away_team.save()
            home_team.save()
        elif instance.result == '2':
            home_team.games_played += 1
            away_team.games_played += 1
            home_team.wins += 1
            home_team.points +=  3
            away_team.losses += 1
            away_team.save()
            home_team.save()
        elif instance.result == '3':
            home_team.games_played += 1
            away_team.games_played += 1
            home_team.draws += 1
            away_team.draws += 1
            home_team.points += 1
            away_team.points += 1
            away_team.save()
            home_team.save()
        else:
            pass




post_save.connect(notify_landlord_or_update_match, sender=Match)
post_save.connect(notify_sponsor_or_update_league, sender=League)
m2m_changed.connect(notify_team_leader, sender=League.teams.through)
