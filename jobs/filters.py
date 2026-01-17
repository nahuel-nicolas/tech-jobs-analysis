from datetime import timedelta
from functools import reduce
import operator

from django.db.models import IntegerField, Min, Q
from django.db.models.functions import Cast, TruncDate
from django.utils import timezone

from configurations.utils import get_job_advanced_filters, get_job_filters, get_job_filter_settings
from jobs.models import Job


def field_contains_any(field, values):
    return reduce(
        operator.or_,
        (Q(**{f"{field}__regex": value}) for value in values)
    )


def field_icontains_any(field, values):
    return reduce(
        operator.or_,
        (Q(**{f"{field}__icontains": value}) for value in values)
    )


def filter_applicants(query):
    return query.annotate(
        applicants_as_int=Cast('applicants', output_field=IntegerField())
    ).filter(
        Q(applicants_as_int__lte=get_job_filter_settings()['max_applicants']) | 
        Q(applicants_as_int__isnull=True)
    )


def filter_company_exclude(query):
    company_exclude = field_icontains_any("company", get_job_filter_settings()['company_exclude'])
    return query.exclude(company_exclude)


def filter_created(query):
    return query.filter(
        created__gte=timezone.now() - timedelta(days=get_job_filter_settings()['max_created_time_days'])
    )


def filter_updated(query):
    return query.filter(
        updated__gte=timezone.now() - timedelta(days=get_job_filter_settings()['max_updated_time_days'])
    )


def filter_description_exclude(query):
    description_exclude = field_icontains_any("description", get_job_filter_settings()['job_exclude'])
    # title is counted as part of description
    title_exclude = field_icontains_any("title", get_job_filter_settings()['job_exclude'])
    return query.exclude(description_exclude | title_exclude)


def filter_description_includes_any(query):
    description_includes_any = field_icontains_any("description", get_job_filter_settings()['job_include_any'])
    # title is counted as part of description
    title_includes_any = field_icontains_any("title", get_job_filter_settings()['job_include_any'])
    return query.filter(description_includes_any | title_includes_any)



def filter_location(query):
    location_has_any = field_icontains_any("location", get_job_filter_settings()['location'])
    return query.filter(location_has_any)


def filter_title_company_distict_jobs(query):
    """Avoid repeated title/company repeated jobs"""
    unique_job_ids = Job.objects.annotate(
        created_date=TruncDate('created')
    ).values(
        'title',
        'company',
    ).annotate(
        min_id=Min('id')
    ).values_list('min_id', flat=True)

    return query.filter(id__in=unique_job_ids)


def filter_title_exclude(query):
    title_exclude = field_icontains_any("title", get_job_filter_settings()['title_exclude'])
    return query.exclude(title_exclude)


FILTERS = [
    filter_applicants,
    filter_company_exclude,
    filter_created,
    filter_updated,
    filter_description_exclude,
    filter_description_includes_any,
    filter_location,
    filter_title_company_distict_jobs,
    filter_title_exclude,
]

def get_base_filtered_jobs():
    filters = [globals()[f] for f in get_job_filters()]
    query = Job.objects
    for filter in filters:
        query = filter(query)
        print(f"{filter.__name__} count: {query.count()}")
    return query


def get_jobs_to_extend():
    return get_base_filtered_jobs().filter(
        extendedjob__isnull=True,
    )


def filter_extended(query):
    query.filter(
        extendedjob__isnull=False,
    )
    return query


def filter_arg_medical_insurance(query):
    description_has_healthcare_names = field_contains_any(
        'description', ['Osde', 'Swiss', 'Omint', 'Sancor', 'OSDE'])
    description_has_healthcare_kw = field_icontains_any(
        'description', 
        [
            'relación dependencia', 
            'relación de dependencia',
            'relacion dependencia',
            'relacion de dependencia',
            'prepaga',
            'obra social',
            'medical insurance',
            'cobertura medica',
        ])
    return query.filter(
        Q(extendedjob__medical_insurance=True) |
        description_has_healthcare_kw | 
        description_has_healthcare_names |
        Q(extendedjob__salary_currency__icontains='ars')
    )


def filter_medical_insurance(query):
    query = query.filter(extendedjob__medical_insurance=True)
    return query


def filter_experience(query):
    query = query.filter(
        Q(extendedjob__min_experience_years__lte=get_job_filter_settings()['max_min_experience_years']) | 
        Q(extendedjob__min_experience_years__isnull=True)
    )
    return query


def filter_education(query):
    query = query.filter(
        extendedjob__bachelor_required=get_job_filter_settings()['exclude_bachelor_required'],
        extendedjob__master_required=get_job_filter_settings()['exclude_master_required'],
        extendedjob__phd_required=get_job_filter_settings()['exclude_phd_required'],
    )
    return query


ADVANCED_FILTERS = [
    filter_extended,
    filter_arg_medical_insurance,
    filter_medical_insurance,
    filter_experience,
    filter_education,
]

def get_filtered_jobs():
    filters = [globals()[f] for f in get_job_advanced_filters()]
    query = get_base_filtered_jobs()

    for filter in filters:
        query = filter(query)
        print(f"{filter.__name__} count: {query.count()}")
    return query


def filter_unviewed_application_status(query):
    query = query.filter(
        Q(applicationstatus__status='unviewed') | 
        Q(applicationstatus__isnull=True)
    )
    return query


def filter_application_status(query, status):
    return query.filter(
        applicationstatus__status=status
    )


def filter_application_status(query, status):
    return query.filter(
        applicationstatus__status=status
    )
