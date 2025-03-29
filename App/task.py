from celery import shared_task
from django.core.management import call_command
from django.utils import timezone
from App.models import LineUpForm, SailedData

# App/celery.py or tasks.py
from celery import shared_task
from django.core.management import call_command

@shared_task
def transfer_sailed_vessels_task():
    call_command('transfer_sailed_vessels')