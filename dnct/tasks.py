from celery import shared_task
from datetime import date
from .models import Funcionariu

@shared_task
def check_birthdays():
    today = date.today()
    employees = Funcionariu.objects.filter(data_do_nasc__month=today.month, data_do_nasc__day=today.day)
    # Implement notification logic here (e.g., email, SMS, etc.)
