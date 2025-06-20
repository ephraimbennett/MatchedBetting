from django.db import models
from home.models import Member

# Create your models here.

class BonusBet(models.Model):
    title = models.TextField(null=True)
    market = models.TextField(null=True)
    time = models.TextField(null=True)
    sport = models.TextField(null=True)

    # the bonus bet
    bonus_bet = models.TextField(null=True)
    bonus_odds = models.IntegerField(null=True)
    bonus_name = models.TextField(null=True)

    hedge_bet = models.TextField(null=True)
    hedge_odds = models.IntegerField(null=True)
    hedge_index = models.FloatField(null=True)
    hedge_name = models.TextField(null=True)

    profit_index = models.FloatField(null=True)

class SecondBet(models.Model):
    title = models.TextField(null=True)
    market = models.TextField(null=True)
    time = models.TextField(null=True)
    sport = models.TextField(null=True)

    # the bonus bet
    bonus_bet = models.TextField(null=True)
    bonus_odds = models.IntegerField(null=True)
    bonus_name = models.TextField(null=True)

    hedge_bet = models.TextField(null=True)
    hedge_odds = models.IntegerField(null=True)
    hedge_name = models.TextField(null=True)

    hedge_index = models.FloatField(null=True)

    profit_index = models.FloatField(null=True)

class ProfitBet(models.Model):
    title = models.TextField(null=True)
    market = models.TextField(null=True)
    time = models.TextField(null=True)
    sport = models.TextField(null=True)

    # the bonus bet
    bonus_bet = models.TextField(null=True)
    bonus_odds = models.IntegerField(null=True)
    bonus_name = models.TextField(null=True)

    hedge_bet = models.TextField(null=True)
    hedge_odds = models.IntegerField(null=True)
    hedge_name = models.TextField(null=True)

    hedge_index = models.FloatField(null=True)

    profit_index = models.FloatField(null=True)

class Promo(models.Model):
    bookmaker = models.TextField()
    description = models.TextField(null=True)
    code = models.CharField(max_length=50, null=True)
    url = models.CharField(max_length=250, null=True)

class State(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)

    value = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class Settings(models.Model):
    user = models.OneToOneField(Member, on_delete=models.CASCADE) # The link to member
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    timezone = models.CharField(default="Etc/GMT+6", max_length=50)

class BookMaker(models.Model):
    title = models.TextField()
    states = models.ManyToManyField(State)

    
class Event(models.Model):
    title = models.TextField(null=True)
    market = models.TextField(null=True)
    time = models.TextField(null=True)
    sport = models.TextField(null=True)

class Line(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='lines')
    bookmaker = models.CharField(max_length=100, null=True)
    side = models.CharField(max_length=100, null=True)
    odds = models.IntegerField(null=True)
