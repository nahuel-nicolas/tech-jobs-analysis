from django.db import migrations
from pathlib import Path


def load_jobs_data(apps, schema_editor):
    sql_file = Path(__file__).resolve().parent.parent.parent / 'jobs_job_202601171446.sql'
    with open(sql_file, 'r') as f:
        sql = f.read()
    connection = schema_editor.connection
    connection.cursor().executescript(sql)


def reverse_load_jobs_data(apps, schema_editor):
    Job = apps.get_model('jobs', 'Job')
    Job.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_jobs_data, reverse_load_jobs_data),
    ]
