# Generated by Django 3.1.4 on 2020-12-17 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20201217_2152'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spends',
            options={'ordering': ['-cost_date']},
        ),
    ]
