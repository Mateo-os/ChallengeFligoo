from rest_framework import serializers
from .models import Game


class BoardField(serializers.Field):
    def to_representation(self, obj):
        # Assuming obj is a 9-character string, convert it to a 3x3 grid
        grid = [obj[i : i + 3] for i in range(0, 9, 3)]
        return grid

    def to_internal_value(self, data):
        # Convert the 3x3 grid back to a 9-character string
        return "".join("".join(row) for row in data)


class GameSerializer(serializers.ModelSerializer):
    board = BoardField(read_only=True)

    class Meta:
        model = Game
        fields = ("id", "starting_token", "board", "players", "turn")
        read_only_fields = ["turn", "active"]


class PlayRequestSerializer(serializers.Serializer):
    player = serializers.IntegerField()
    row = serializers.IntegerField()
    column = serializers.IntegerField()

    class Meta:
        fields = ("player_id", "row", "column")


class PlayResponseSerializer(serializers.ModelSerializer):
    board = BoardField(read_only=True)
    active_player = serializers.SerializerMethodField()

    def get_active_player(self, obj):
        players = obj.players.all()
        num_players = len(players)
        if num_players == 2:
            player_names = [player.name for player in players]
            current_player_index = obj.turn % num_players
            return player_names[current_player_index]
        return None

    class Meta:
        model = Game
        fields = (
            "id",
            "starting_token",
            "board",
            "players",
            "active_player",
            "turn",
        )
        read_only_fields = ["turn"]
