# Generated by Django 5.0.1 on 2024-01-17 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_alter_game_starting_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='board',
            field=models.CharField(blank=True, default='---------', max_length=9),
        ),
    ]
