# Generated by Django 3.2 on 2022-11-11 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('industrial', '0015_auto_20221111_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='status',
            field=models.CharField(choices=[('published', 'Опубликована'), ('not_published', 'Не опубликована')], default='Опубликована', max_length=20),
        ),
    ]
