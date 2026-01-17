import logging

from django.core.management.base import BaseCommand

from jobs.utils import get_jobs_to_extend

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Print Jobs ready to be extended'
    def handle(self, *args, **options):
        pretty_print_jobs([
            dict(
                title=job.title,
                company=job.company,
                location=job.location
            ) for job in get_jobs_to_extend()
        ])

def pretty_print_jobs(jobs_list):
    for i, job in enumerate(jobs_list):
        print(f" title: '{job['title']}'")
        print(f" company: '{job['company']}'")
        print(f" location: '{job['location']}'")
        print()  # Extra line between job entries
    print(str(len(jobs_list)) + " jobs")