# Generated by Django 4.2 on 2023-05-23 21:55

import authentication.utils.enums.level
import authentication.utils.enums.vulnerability
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Companie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('is_tested', models.BooleanField(default=False)),
                ('created_at', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReportVulnerability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vulnerability', models.CharField(default=authentication.utils.enums.vulnerability.Vulnerability['other'], max_length=42, verbose_name=authentication.utils.enums.vulnerability.Vulnerability)),
                ('description', models.CharField(max_length=200)),
                ('level', models.CharField(default=authentication.utils.enums.level.Level['low'], max_length=6, verbose_name=authentication.utils.enums.level.Level)),
                ('created_in', models.DateTimeField(auto_now_add=True)),
                ('companie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.companie')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
