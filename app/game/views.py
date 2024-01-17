from rest_framework import viewsets
from rest_framework.routers import DefaultRouter

from .models import Game
from .serializers import GameSerializer


class GameView(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all()


router = DefaultRouter()
router.register('', GameView, basename='games')
