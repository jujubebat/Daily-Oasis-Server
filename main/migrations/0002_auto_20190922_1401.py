# Generated by Django 2.2.4 on 2019-09-22 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=12, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=12, max_digits=20, null=True),
        ),
    ]
