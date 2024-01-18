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

    def create_response(self, game, message, code):
        response_serializer = GameSerializer(game)
        data = response_serializer.data
        data["message"] = message
        return Response(data, code)

    @action(detail=True, methods=["post", "get"])
    def play(self, request, pk=None):
        game: Game = self.get_object()
        if not game.active:
            return self.create_response(game, "This game has ended", 200)
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
        turn_parity = game.turn % 2
        if player != game.players.all()[turn_parity]:
            return self.create_response(game, "Is not this players turn to move!", 200)

        # Check if the move is valid
        row = int(validated_data["row"]) - 1
        column = int(request.data["column"]) - 1
        if not (0 <= row <= 8 and 0 <= column <= 8):
            return self.create_response(
                game, "Row and column value must be between 1 and 9", 00
            )

        if game.board[3 * row + column] != BLANK:
            return self.create_response(
                game, "Invalid move. Cell already occupied.", status=200
            )

        # Make the move
        game.move(token, row, column)
        game.turn += 1
        game.save()

        # Check for game over conditions
        message = ""
        if game.is_win_state():
            game.active = False
            game.save()
            message = f"Player {player.name} wins!"
        elif game.is_full():
            game.active = False
            game.save()
            message = "It's a draw!"
        else:
            message = "Move was succesfull!. The game continues"
        return self.create_response(game, message, 200)


router = DefaultRouter()
router.register(r"games", GameView, basename="game")
