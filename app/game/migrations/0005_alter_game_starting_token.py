# Generated by Django 5.0.1 on 2024-01-17 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_alter_game_board'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='starting_token',
            field=models.CharField(choices=[('X', 'X'), ('O', 'O')], max_length=1),
        ),
    ]
