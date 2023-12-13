# Generated by Django 3.2 on 2022-11-16 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20221116_1101'),
        ('industrial', '0019_auto_20221116_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyfinancetransaction',
            name='payment_for_job',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment', to='industrial.job'),
        ),
        migrations.AlterField(
            model_name='companyfinancetransaction',
            name='payment_invoice',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transaction', to='payment.paymentinvoice'),
        ),
    ]