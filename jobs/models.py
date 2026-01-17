from django.db import models
from utils.models import TimeStampedModel

class Job(TimeStampedModel):
    LINKEDIN = 'linkedin'
    INDEED = 'indeed'
    STACK = 'stack'
    PORTAL_CHOICES = [
        (LINKEDIN, 'Linkedin'),
        (INDEED, 'Indeed'),
        (STACK, 'Stack Overflow'),
    ]

    portal_id = models.CharField(unique=True)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True, default=None)
    description = models.TextField()
    applicants = models.CharField(max_length=255, blank=True, null=True, default=None)
    query = models.IntegerField(blank=True, null=True, default=None)
    portal = models.CharField(
        max_length=20,
        choices=PORTAL_CHOICES,
        default=LINKEDIN,
    )
    salary = models.CharField(max_length=255, default=None, null=True, blank=True)

class ExtendedJob(TimeStampedModel):
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    bachelor_required = models.BooleanField()
    master_required = models.BooleanField()
    phd_required = models.BooleanField()
    tech_stack = models.CharField(max_length=255, default=None, null=True, blank=True)
    min_experience_years = models.IntegerField(default=None, null=True, blank=True)
    us_only = models.BooleanField()
    salary = models.CharField(max_length=255, default=None, null=True, blank=True)
    employment_type = models.CharField(max_length=255, default=None, null=True, blank=True)
    medical_insurance = models.BooleanField()
    hourprice = models.FloatField(default=None, null=True, blank=True)
    salary_currency = models.CharField(max_length=255, default=None, null=True, blank=True)
