# Generated by Django 2.1.15 on 2020-12-03 04:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.Location'),
        ),
    ]
