# Generated by Django 3.2.5 on 2021-07-20 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='location_node_id',
            field=models.BigIntegerField(default=123548698, verbose_name='loaction node id'),
            preserve_default=False,
        ),
    ]