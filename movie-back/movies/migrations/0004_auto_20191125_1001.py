# Generated by Django 2.2.5 on 2019-11-25 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20191125_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='audience',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
