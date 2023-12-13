# Generated by Django 3.2 on 2022-11-21 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_base', '0016_alter_individualtag_title'),
        ('industrial', '0025_auto_20221119_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='all_ind_tags',
            field=models.ManyToManyField(null=True, related_name='all_ind_job_tegs', to='core_base.IndividualTag'),
        ),
        migrations.AlterField(
            model_name='job',
            name='ind_tags',
            field=models.ManyToManyField(null=True, related_name='ind_job_tegs', to='core_base.IndividualTag'),
        ),
        migrations.AlterField(
            model_name='job',
            name='tags',
            field=models.ManyToManyField(null=True, related_name='job_tegs', to='core_base.Tag'),
        ),
    ]
