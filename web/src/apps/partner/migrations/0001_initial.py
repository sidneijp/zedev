# Generated by Django 3.1.2 on 2020-10-12 00:28

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tradingName', models.CharField(max_length=100)),
                ('ownerName', models.CharField(max_length=50)),
                ('document', models.CharField(max_length=14)),
                ('coverageArea', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('address', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'verbose_name': 'Partner',
                'verbose_name_plural': 'Partners',
            },
        ),
    ]
