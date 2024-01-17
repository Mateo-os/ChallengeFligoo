from rest_framework import serializers
from .models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ("id", "starting_token", "board", "players", "turn")
        read_only_fields = ("board", "turn")


class PlayRequestSerializer(serializers.Serializer):
    player = serializers.IntegerField()
    row = serializers.IntegerField()
    column = serializers.IntegerField()

    class Meta:
        fields = ("player_id", "row", "column")
