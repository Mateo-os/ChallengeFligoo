from django.contrib import admin
from django.urls import path,include
from player.views import router as playerRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/players/', include(playerRouter.urls))
]
