# Generated by Django 3.2 on 2022-11-27 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0006_alter_seometa_meta_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seometa',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='meta_images'),
        ),
    ]