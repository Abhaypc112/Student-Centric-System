# Generated by Django 3.0.5 on 2024-01-26 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='status2',
            field=models.BooleanField(default=False),
        ),
    ]