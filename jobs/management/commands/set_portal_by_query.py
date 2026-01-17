import logging

from django.core.management.base import BaseCommand

from jobs.models import Job
from utils.utils import get_hostname
from django.conf import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Set Job.portal based on Job.query.url'
    def handle(self, *args, **options):
        for job in Job.objects.all().select_related("query"):
            query_hostname = get_hostname(job.query.url)
            if query_hostname not in settings.VALID_PORTALS:
                print(f"Job {job.id} - {query_hostname} is not valid")
                continue
            job.portal = query_hostname
            job.save()
            print(f"Job: {job.id} - Portal: {query_hostname}")
