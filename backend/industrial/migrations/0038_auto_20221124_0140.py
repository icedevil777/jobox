# Generated by Django 3.2 on 2022-11-24 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('industrial', '0037_auto_20221124_0123'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='seo_image',
            field=models.FileField(null=True, upload_to='meta_images'),
        ),
        migrations.AlterField(
            model_name='job',
            name='seo_description',
            field=models.CharField(blank=True, max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='seo_keywords',
            field=models.CharField(blank=True, max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='seo_title',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
