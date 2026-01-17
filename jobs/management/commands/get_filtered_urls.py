import logging
from pprint import pprint

from django.core.management.base import BaseCommand

from jobs.utils import get_job_obj_url
from jobs.filters import get_filtered_jobs


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Creates ExtendedJob records for Job entries that do not have them'

    def handle(self, *args, **options):
        jobs = get_filtered_jobs()
        job_list = []
        for job in jobs:
            job_dict = dict(
                title=job.title,
                company=job.company,
                applicants=job.applicants,
                url=get_job_obj_url(job)
            )
            job_list.append(job_dict)
        pprint(job_list)
