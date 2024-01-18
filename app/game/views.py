from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from player.models import Player

from .models import Game, BLANK
from .serializers import GameSerializer, PlayRequestSerializer


class GameView(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all()

    @action(detail=True, methods=["post", "get"])
    def play(self, request, pk=None):
        game: Game = self.get_object()
        if not game.active:
            return Response({"error": "This game has ended"}, 400)
        # Validate the incoming data using PlayRequestSerializer
        serializer = PlayRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, 400)
        token = (
            game.starting_token
            if game.turn % 2 == 0
            else "XO".replace(game.starting_token, "")
        )
        validated_data = serializer.validated_data
        player_id = validated_data["player"]  # Include the player ID making the move

        # Find the player making the move
        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return Response({"error": "Player does not exist"}, 400)
        # Check if player in the game
        if player not in game.players.all():
            return Response({"error": "Player not in game"}, 400)

        # Check if it's the player's turn
        if game.turn % 2 == 0 and player != game.players.all()[0]:
            return Response({"error": "Not the player's turn to move."}, status=400)
        elif game.turn % 2 == 1 and player != game.players.all()[1]:
            return Response({"error": "Not the player's turn to move."}, status=400)

        # Check if the move is valid
        row = validated_data["row"] - 1
        column = request.data["column"] - 1
        if not (0 <= row <= 8 and 0 <= column <= 8):
            return Response({"error": "Row and column value must be between 1 and 9"})

        if game.board[3 * row + column] != BLANK:
            return Response(
                {"error": "Invalid move. Cell already occupied."}, status=400
            )

        # Make the move
        game.move(token, row, column)
        game.turn += 1
        game.save()

        # Check for game over conditions
        if game.is_win_state():
            game.active = False
            game.save()
            return Response({"message": f"Player {player.name} wins!"}, status=200)
        elif game.is_full():
            game.active = False
            game.save()
            return Response({"message": "It's a draw!"}, status=200)
        else:
            return Response(
                {"message": "Move successful. Game in progress."}, status=200
            )


router = DefaultRouter()
router.register(r"games", GameView, basename="game")
