# Generated by Django 3.2 on 2022-11-21 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_base', '0016_alter_individualtag_title'),
        ('industrial', '0030_auto_20221121_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='all_ind_tags',
            field=models.ManyToManyField(related_name='all_ind_job_tegs', to='core_base.IndividualTag'),
        ),
        migrations.AlterField(
            model_name='job',
            name='ind_tags',
            field=models.ManyToManyField(related_name='ind_job_tegs', to='core_base.IndividualTag'),
        ),
    ]
