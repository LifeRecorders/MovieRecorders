# Generated by Django 2.2.5 on 2019-11-26 03:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0014_movie_naver_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='movies.Review'),
        ),
    ]
