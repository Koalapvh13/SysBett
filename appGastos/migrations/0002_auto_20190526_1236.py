# Generated by Django 2.2.1 on 2019-05-26 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appGastos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='nome',
            field=models.CharField(default=None, max_length=80, unique=True, verbose_name='Nome'),
        ),
    ]
