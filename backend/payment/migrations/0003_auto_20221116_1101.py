# Generated by Django 3.2 on 2022-11-16 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('industrial', '0018_auto_20221116_1056'),
        ('payment', '0002_alter_paymentinvoice_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentinvoice',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='payment_invoices', to='industrial.company'),
        ),
        migrations.AlterField(
            model_name='tinkoffcardpayment',
            name='payment_invoice',
            field=models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='tinkoff_card_payment', to='payment.paymentinvoice'),
        ),
    ]
