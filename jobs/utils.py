from jobs.models import Job


def get_jobs_to_extend():
    return Job.objects.filter(
        extendedjob__isnull=True,
        salary__isnull=False
    )
