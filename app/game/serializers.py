from rest_framework import serializers
from .models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'starting_token', 'players')
        read_only_fields = ('board', 'turn')
