# Generated by Django 3.2 on 2022-11-21 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_base', '0016_alter_individualtag_title'),
        ('industrial', '0027_auto_20221121_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='tags',
            field=models.ManyToManyField(related_name='job_tegs', to='core_base.Tag'),
        ),
    ]
