# Generated by Django 5.0 on 2023-12-13 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='compleated',
            field=models.BooleanField(default=False),
        ),
    ]
