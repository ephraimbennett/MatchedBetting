from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),
    path('bonus_bets/', views.bonus_bets, name='bonus_bets'),
    path('second_chance', views.second_chance, name='second_chance'),
    path('profit_boost', views.profit_boost, name='profit_boost'),
    path('prompt/', views.prompt_action, name='prompt')
]