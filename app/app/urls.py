from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from player.views import router as player_router
from game.views import router as game_router

api_router = DefaultRouter()
api_router.registry.extend(player_router.registry)
api_router.registry.extend(game_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_router.urls)),
]
