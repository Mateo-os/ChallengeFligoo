from rest_framework import viewsets
from rest_framework.routers import DefaultRouter

from .models import Player
from .serializers import PlayerSerializer


class PlayerView(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()


router = DefaultRouter()
router.register(r"players", PlayerView, basename="player")
