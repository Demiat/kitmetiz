import logging

from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from core.funcs import process_exchange_1C

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

NAME_JOB_1C_EXCHANGE = 'exchange_1c_job'
NAME_JOB_EXECUTIONS = 'delete_old_job_executions'


def exchange_1c_job():
    """Обмен данными JSON из 1С."""
    print(process_exchange_1C())


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """Удаляет старые записи из модели о выполненных операциях."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = 'Обмен данными с 1С'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), 'default')

        scheduler.add_job(
            exchange_1c_job,
            trigger=CronTrigger(minute="*/1"),
            id=NAME_JOB_1C_EXCHANGE,  # уникальное имя работы
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id=NAME_JOB_EXECUTIONS,
            max_instances=1,
            replace_existing=True,
        )

        try:
            scheduler.start()
        except KeyboardInterrupt:
            logger.info('Останавливаем планировщик...')
            scheduler.shutdown()
