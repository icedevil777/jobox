# Generated by Django 3.2 on 2022-11-18 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0003_merge_0002_alter_templateparts_options_0002_indexfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeoMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_type', models.CharField(choices=[('title', 'title'), ('description', 'description'), ('keywords', 'keywords')], max_length=20)),
                ('path', models.CharField(max_length=150)),
                ('content', models.TextField(max_length=50000)),
            ],
        ),
    ]
