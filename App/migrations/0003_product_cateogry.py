# Generated by Django 4.0.4 on 2022-09-07 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_cateogry'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cateogry',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='App.cateogry'),
        ),
    ]
