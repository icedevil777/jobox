# Generated by Django 3.2 on 2022-10-27 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('industrial', '0008_rename_tags_job_job_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='about_education',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='about_experience',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='about_app',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
