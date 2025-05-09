from celery import shared_task
from .services import update_bets, update_promos

@shared_task
def test_task():
    print("Initializing...")
    #update_bets()

@shared_task
def promos_update():
    update_promos()