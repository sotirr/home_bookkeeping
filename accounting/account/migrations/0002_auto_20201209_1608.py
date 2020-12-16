# Generated by Django 3.1.4 on 2020-12-09 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categories',
            old_name='category',
            new_name='category_name',
        ),
        migrations.AlterField(
            model_name='spends',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.categories'),
        ),
        migrations.AlterField(
            model_name='spends',
            name='payer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.payers'),
        ),
    ]
