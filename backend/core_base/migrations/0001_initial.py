# Generated by Django 3.2 on 2022-10-20 14:54

import core_base.models
import core_base.querysets.user
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalSalaryCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Доп. условие по зарплате',
                'verbose_name_plural': 'Доп. условие по зарплате',
            },
        ),
        migrations.CreateModel(
            name='ApplicationsToAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=150)),
                ('text', models.TextField(max_length=2048)),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки Администратору',
            },
        ),
        migrations.CreateModel(
            name='BlogAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_ad', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'БЛОГ Автор',
                'verbose_name_plural': 'БЛОГ Автор',
            },
        ),
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'БЛОГ Категория',
                'verbose_name_plural': 'БЛОГ Категории',
            },
        ),
        migrations.CreateModel(
            name='CommunicationMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=20)),
                ('icon_code', models.CharField(max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Cпособ связи',
                'verbose_name_plural': 'Cпособ связи',
            },
        ),
        migrations.CreateModel(
            name='EmploymentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Тип занятости',
                'verbose_name_plural': 'Тип занятости',
            },
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Опыт работы',
                'verbose_name_plural': 'Опыт работы',
            },
        ),
        migrations.CreateModel(
            name='JobCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('icon_code', models.CharField(blank=True, max_length=100, null=True)),
                ('show_on_main_page', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категория',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(blank=True, db_index=True, max_length=50, null=True, verbose_name='Регион')),
                ('region_type', models.CharField(blank=True, db_index=True, max_length=10, null=True)),
                ('city', models.CharField(db_index=True, max_length=150, verbose_name='Город')),
                ('foundation_year', models.IntegerField(blank=True, null=True)),
                ('population', models.IntegerField(blank=True, null=True)),
                ('geo_lon', models.FloatField(blank=True, null=True)),
                ('geo_lat', models.FloatField(blank=True, null=True)),
                ('timezone', models.CharField(blank=True, max_length=10, null=True)),
                ('tax_office', models.CharField(blank=True, max_length=10, null=True)),
                ('oktmo', models.CharField(blank=True, max_length=20, null=True)),
                ('okato', models.CharField(blank=True, max_length=20, null=True)),
                ('capital_marker', models.IntegerField(blank=True, null=True)),
                ('fias_level', models.IntegerField(blank=True, null=True)),
                ('fias_id', models.CharField(blank=True, max_length=50, null=True)),
                ('kladr_id', models.BigIntegerField(blank=True, null=True)),
                ('city_name', models.CharField(blank=True, max_length=100, null=True)),
                ('city_type', models.CharField(blank=True, max_length=10, null=True)),
                ('area', models.CharField(blank=True, max_length=100, null=True)),
                ('area_type', models.CharField(blank=True, max_length=10, null=True)),
                ('federal_district', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, db_index=True, max_length=150, null=True, verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='SalarySize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('max_salary', models.IntegerField(default=10000000)),
                ('min_salary', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Мин и мах зарплата',
                'verbose_name_plural': 'Мин и мах зарплата',
            },
        ),
        migrations.CreateModel(
            name='SystemImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('file', models.FileField(upload_to='system_images')),
                ('width', models.CharField(blank=True, max_length=50, null=True)),
                ('height', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('show_on_main_page', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='WorkSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'График работы',
                'verbose_name_plural': 'График работы',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_ad', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250)),
                ('subtitle', models.CharField(max_length=500)),
                ('main_image', models.ImageField(upload_to='blog/images')),
                ('body', models.TextField()),
                ('show_on_main_page', models.BooleanField(default=False, verbose_name='на главной странице')),
                ('show_on_for_company_page', models.BooleanField(default=False, verbose_name='на страницу для работодателей')),
                ('show_sing_in_on_company_page', models.BooleanField(default=False, verbose_name="Кнопка 'вход в личный кабинет'")),
                ('show_on_news_page', models.BooleanField(default=False, verbose_name='на странице новостей')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='blogs', to='core_base.blogauthor')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to='core_base.blogcategory')),
            ],
            options={
                'verbose_name': 'БЛОГ Пост',
                'verbose_name_plural': 'БЛОГ Посты',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('IND', 'Industrial'), ('APPLICANT', 'Applicant')], max_length=20)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_email_confirmed', models.BooleanField(default=False)),
                ('email_confirm_code', models.CharField(default=core_base.models.generate_email_confirmation_code, max_length=40)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', core_base.querysets.user.CustomUserManager()),
            ],
        ),
    ]
