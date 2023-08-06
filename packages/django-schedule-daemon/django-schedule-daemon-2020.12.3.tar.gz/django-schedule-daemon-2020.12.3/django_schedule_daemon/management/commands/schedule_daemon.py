import logging
import os
import schedule
import time

from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        __import__(os.environ['DJANGO_SCHEDULE_MODULE'])
        while True:
            try:
                schedule.run_pending()
            except Exception as e:
                print('%s: %s' % (type(e),str(e)))
                logging.error(e, exc_info=True)
            finally:
                time.sleep(1)

