from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),
    path('bonus_bets/', views.bonus_bets, name='bonus_bets'),
    path('second_chance', views.second_chance, name='second_chance')
]