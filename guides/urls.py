from django.urls import path
from . import views

urlpatterns = [
    path('guides/', views.guides_list, name='guides_list'),
    path('guides/search/', views.search, name='guides_search'),
    path('guides/<slug:slug>/', views.guides_detail, name='guides_detail')
    
]
