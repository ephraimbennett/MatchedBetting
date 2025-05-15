from django.contrib import admin
from .models import Settings, BonusBet, SecondBet, State, ProfitBet

# Register your models here.
admin.site.register(BonusBet)
admin.site.register(Settings)
admin.site.register(SecondBet)
admin.site.register(State)
admin.site.register(ProfitBet)