from django.contrib import admin
from django.urls import path,include
from player.views import router as playerRouter
from game.views import router as gameRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/players/', include(playerRouter.urls)),
    path('api/games/', include(gameRouter.urls))
]
