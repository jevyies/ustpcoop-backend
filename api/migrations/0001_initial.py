# Generated by Django 4.1.5 on 2023-02-06 11:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_no', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=200)),
                ('image_path', models.CharField(blank=True, max_length=500, null=True)),
                ('date_registered', models.DateField(default=datetime.date.today)),
                ('date_approved', models.DateField(blank=True, null=True)),
                ('account_type', models.CharField(default='member', max_length=10)),
                ('account_status', models.CharField(default='pending', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='WithdrawalSlip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_requested', models.DateField(default=datetime.date.today)),
                ('total_amount', models.CharField(max_length=500)),
                ('image_path_passed', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(default='pending', max_length=10)),
                ('date_approved', models.DateField(blank=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.account')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_remarks', models.TextField(blank=True, null=True)),
                ('date_requested', models.DateField(default=datetime.date.today)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.account')),
            ],
        ),
        migrations.CreateModel(
            name='DepositSlip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_requested', models.DateField(default=datetime.date.today)),
                ('total_amount', models.CharField(max_length=500)),
                ('image_path_passed', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(default='pending', max_length=10)),
                ('date_approved', models.DateField(blank=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.account')),
            ],
        ),
    ]