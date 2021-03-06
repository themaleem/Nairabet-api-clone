# Generated by Django 3.0.5 on 2020-04-05 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('betcore', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='League',
            new_name='league',
        ),
        migrations.AddField(
            model_name='league',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='betcore.Category'),
            preserve_default=False,
        ),
    ]
