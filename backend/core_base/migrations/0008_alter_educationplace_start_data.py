# Generated by Django 3.2 on 2022-11-01 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_base', '0007_alter_educationplace_start_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationplace',
            name='start_data',
            field=models.DateField(),
        ),
    ]
