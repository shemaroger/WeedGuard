# Generated by Django 5.1.2 on 2024-11-18 20:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weedGuardApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('farmer', 'Farmer')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.AlterModelOptions(
            name='prediction',
            options={'verbose_name': 'Prediction', 'verbose_name_plural': 'Predictions'},
        ),
        migrations.RemoveField(
            model_name='prediction',
            name='farmer',
        ),
        migrations.AddField(
            model_name='prediction',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='weedGuardApp.user'),
        ),
    ]
