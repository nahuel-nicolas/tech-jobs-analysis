import logging
import json

from django.conf import settings
from django.core.management.base import BaseCommand

from openai import OpenAI

from jobs.models import ExtendedJob
from jobs.filters import get_jobs_to_extend


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Creates ExtendedJob records for Job entries that do not have them'

    def handle(self, *args, **options):
        extend_jobs()

def is_openai_config():
    if not settings.OPEN_AI_API_KEY:
        return False
    if not settings.OPEN_AI_MODEL:
        return False
    return True

def check_openai_config():
    if not is_openai_config():
        raise ValueError("Error: Missing OpenAI config.")

check_openai_config()
client = OpenAI(api_key=settings.OPEN_AI_API_KEY)


def get_extended_jobs(jobs, request_limit):
    extended_jobs = []
    counter = 0
    jobs_count = len(jobs)
    print(f"Found {jobs_count} jobs to process.")
    for job in jobs:
        counter += 1
        if counter >= request_limit:
            print(f"Request Limit ({request_limit}) reached.")
            break
        initial_prompt = """
        be ready for: reading a text input, it is gonna be a job post text
        then answer with this json structure:
        {
            bachelor_required: bool, (true if bachelor is required or master is prefered)
            master_required: bool, (true if master is required or phd prefered)
            phd_required: bool,
            tech_stack: str | null, (e.g. 'javascript,python,react,etc')
            min_experience_years: int, (default 0)
            us_only: bool,
            salary: str | null, (if no numbers, then null)
            employment_type: str | null, (e.g. 'full-time' | 'part-time' | 'contract' | null)
            medical_insurance: bool, (is medical insurance listed as a benefit?)
            hourprice: float | null, (how much do they pay per hour?)
            salary_currency: str | null, (e.g. 'usd' | 'usd,ars,cad,etc' | null)
        }
        just return the json not an string with extra words like 'json'
        """
        print(f"Processing job w/ id {job.portal_id} {counter}/{jobs_count}")
        
        response = client.chat.completions.create(
            model=settings.OPEN_AI_MODEL,
            messages=[
                {"role": "system", "content": initial_prompt},
                {"role": "user", "content": job.description}
            ]
        )
        try:
            response_data = json.loads(
                response.choices[0].message.content.replace("json", "", 1).replace("```", "", 2).strip()
            )
            try:
                extended_job, _ = ExtendedJob.objects.update_or_create(
                    job=job,
                    **response_data
                )
                extended_jobs.append(extended_job)
            except Exception as e:
                print(f"An error occurred while saving extended job: {job.id}, error: {e}")
        except Exception as e:
            print(f"An error occurred while parsing AI response: {job.id}, error: {e}")
            print(type(response.choices[0].message.content))
            print(response.choices[0].message.content)
    return extended_jobs

def extend_jobs(request_limit=float("inf")):
    jobs = get_jobs_to_extend()
    if not jobs:
        raise ValueError(f"No jobs to process {len(jobs)}")
    processed_jobs = get_extended_jobs(jobs, request_limit)
    if not processed_jobs:
        print("ERROR: No processed data")
        raise ValueError(f"No processed data {len(processed_jobs)}")
    return processed_jobs
