# Generated by Django 4.2.13 on 2024-05-16 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='odigranaigra',
            name='RedniBrojIgre',
            field=models.IntegerField(default=99),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='odigranaigra',
            name='Igrac1Poeni',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='odigranaigra',
            name='Igrac2Poeni',
            field=models.IntegerField(null=True),
        ),
    ]
