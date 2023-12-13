# Generated by Django 3.2 on 2022-11-11 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('industrial', '0015_auto_20221111_1447'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentinvoice',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_invoices', to='industrial.company'),
        ),
    ]
