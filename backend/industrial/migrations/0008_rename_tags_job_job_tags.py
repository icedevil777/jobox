# Generated by Django 3.2 on 2022-10-27 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('industrial', '0007_auto_20221027_0836'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='tags_job',
            new_name='tags',
        ),
    ]
