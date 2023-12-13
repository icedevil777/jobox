# Generated by Django 3.2 on 2022-11-18 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0005_seometa_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seometa',
            name='meta_type',
            field=models.CharField(choices=[('title', 'title'), ('description', 'description'), ('keywords', 'keywords'), ('image', 'image')], max_length=20),
        ),
    ]
