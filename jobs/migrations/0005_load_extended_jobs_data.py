from django.db import migrations
from pathlib import Path


def load_extended_jobs_data(apps, schema_editor):
    sql_file = Path(__file__).resolve().parent.parent.parent / 'jobs_extendedjob_202601311441.sql'
    with open(sql_file, 'r') as f:
        sql = f.read()
    connection = schema_editor.connection
    connection.cursor().executescript(sql)


def reverse_load_extended_jobs_data(apps, schema_editor):
    ExtendedJob = apps.get_model('jobs', 'ExtendedJob')
    ExtendedJob.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_alter_extendedjob_bachelor_required_and_more'),
    ]

    operations = [
        migrations.RunPython(load_extended_jobs_data, reverse_load_extended_jobs_data),
    ]
