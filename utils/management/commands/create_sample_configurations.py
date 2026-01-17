import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from configurations.models import (
    JobFilter,
    JobFilterGroup,
    JobFilterSettings,
    ScraperGroup,
    ScraperGroupSearch,
    ScraperSearch
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Creates the sample scraper and job filter configuration.'

    def handle(self, *args, **options):
        create_sample_configurations()


def create_sample_configurations():
    """
    Creates the sample scraper and job filter configuration.
    This function is idempotent - it won't create duplicates if run multiple times.
    This is the configuration a Django & React Dev would use to find jobs w/ argentine healthcare.
    """
    
    # Use transaction to ensure data consistency
    with transaction.atomic():
        
        # 1. Create ScraperSearch objects
        scraper_search_1, created = ScraperSearch.objects.get_or_create(
            name="Linkedin - Django React - Full Stack - Any ARG",
            defaults={
                'portal': ScraperSearch.LINKEDIN,
                'keywords': ['full stack', 'python', 'react', 'django'],
                'date_posted': ScraperSearch.WEEK,
                'location': 'Argentina',
                'work_type': ScraperSearch.ANY,
                'sort_type': ScraperSearch.RELEVANCE,
                'start_by': 0,
                'max_jobs': 300,
            }
        )
        
        scraper_search_2, created = ScraperSearch.objects.get_or_create(
            name="Indeed - Django React - Full Stack - Any ARG",
            defaults={
                'portal': ScraperSearch.INDEED,
                'keywords': ['full stack', 'python', 'react', 'django'],
                'date_posted': ScraperSearch.TWO_WEEKS,
                'location': 'Argentina',
                'work_type': ScraperSearch.ANY,
                'sort_type': ScraperSearch.RELEVANCE,
                'start_by': 0,
                'max_jobs': 50,
            }
        )
        
        # 2. Create ScraperGroup
        scraper_group, created = ScraperGroup.objects.get_or_create(
            name="Django React - Full Stack - Argentina",
            defaults={
                'active': True,
            }
        )
        
        # 3. Create ScraperGroupSearch relationships (through model)
        scraper_group_search_1, created = ScraperGroupSearch.objects.get_or_create(
            group=scraper_group,
            search=scraper_search_2,  # Indeed search (id=2 in your data)
            defaults={
                'order': 0,
            }
        )
        
        scraper_group_search_2, created = ScraperGroupSearch.objects.get_or_create(
            group=scraper_group,
            search=scraper_search_1,  # LinkedIn search (id=1 in your data)
            defaults={
                'order': 1,
            }
        )
        
        # 4. Create JobFilterSettings
        job_filter_settings, created = JobFilterSettings.objects.get_or_create(
            name="Django React Dev",
            defaults={
                'settings': {
                    'company_exclude': [
                        'Lumenalta', 'Canonical', 'micro1', 'dev.pro', 'auditboard',
                        'The Credit Pros', 'Oowlish', 'BairesDev', 'Cosign', 'Odin AI',
                        'Tribal Worldwide Guatemala', 'Puzzle', 'CookUnity', 'SOOFT Technology',
                        'Kajae', 'Worldly', 'C&S Informática'
                    ],
                    'job_exclude': ['shopify'],
                    'job_include_any': [
                        'Python', 'React', 'Django', 'Vue', 'FullStack', 'full-stack',
                        'Full stack', 'frontend', 'front-end', 'front end', 'backend',
                        'back-end', 'back end', 'Developer', 'programador', 'software engineer'
                    ],
                    'location': [
                        'desde casa', 'remote', 'cordoba', 'córdoba', 'argentina', 'latin america'
                    ],
                    'max_applicants': 99,
                    'max_created_time_days': 30,
                    'max_updated_time_days': 30,
                    'title_exclude': [
                        'C#', 'laravel', ' bi ', 'GEN AI', 'GENAI', 'C++', 'rust', 'lang',
                        'etl', 'ruby', '.net', 'php', 'shopify', 'wordpress', 'android',
                        'Kotlin', 'ios', 'Flutter', 'mobile', 'low-code', 'no-code',
                        'snowflake', 'java', 'salesforce', 'Analytics', 'robotic',
                        'React Native', 'scala', 'drupal', 'roku', 'replit', 'cms',
                        'ror', 'aplicaciones', 'net suite', 'mulesoft', 'sdet', 'scrum',
                        'magento', 'meta4', 'cobol', 'lead', 'DevOps', 'sre', 'ML',
                        'Machine Learning', 'Data Engineer', 'QA', 'Research', 'Manager',
                        'Quality Assurance', 'owner', 'designer', 'lider', 'Architect',
                        'principal', 'cto', 'dba', 'Data Scientist', 'DevSecOps', 'Líder',
                        'Analyst', 'SYSTEMS ENGINEER', 'Support', 'technical', 'product',
                        'testing', 'representative', 'Reliability', 'security',
                        'Infrastructure', 'cloud', 'consultor', 'trading', 'quality',
                        'manger', 'evangelist', 'automation', 'platform', 'profesor',
                        'head', 'sysadmin', 'marketing', 'consult', 'sales', 'database',
                        'test', 'automati', 'talent pool', 'chinese', 'imagenes'
                    ]
                }
            }
        )
        
        # 5. Create JobFilter
        job_filter, created = JobFilter.objects.get_or_create(
            name="Django Python Dev ARG Healthcare",
            defaults={
                'filters': [
                    'filter_company_exclude',
                    'filter_updated',
                    'filter_description_exclude',
                    'filter_description_includes_any',
                    'filter_location',
                    'filter_title_company_distict_jobs',
                    'filter_title_exclude'
                ],
                'advanced_filters': [
                    'filter_extended',
                    'filter_arg_medical_insurance'
                ]
            }
        )
        
        # 6. Create JobFilterGroup
        job_filter_group, created = JobFilterGroup.objects.get_or_create(
            name="Django React Dev - ARG Healthcare",
            defaults={
                'active': True,
                'job_filter': job_filter,
                'job_filter_settings': job_filter_settings,
            }
        )
        
        print("Sample data created successfully!")
        print(f"Created ScraperSearch objects: {scraper_search_1.name}, {scraper_search_2.name}")
        print(f"Created ScraperGroup: {scraper_group.name}")
        print(f"Created JobFilter: {job_filter.name}")
        print(f"Created JobFilterSettings: {job_filter_settings.name}")
        print(f"Created JobFilterGroup: {job_filter_group.name}")
        
        return {
            'scraper_searches': [scraper_search_1, scraper_search_2],
            'scraper_group': scraper_group,
            'job_filter': job_filter,
            'job_filter_settings': job_filter_settings,
            'job_filter_group': job_filter_group,
        }