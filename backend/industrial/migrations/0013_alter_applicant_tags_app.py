# Generated by Django 3.2 on 2022-11-03 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_base', '0009_remove_educationplace_have_education'),
        ('industrial', '0012_auto_20221101_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='tags_app',
            field=models.ManyToManyField(related_name='tags_app', to='core_base.TagApp'),
        ),
    ]
