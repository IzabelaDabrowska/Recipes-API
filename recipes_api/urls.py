from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import AppUserViewSet

def_router = DefaultRouter()
def_router.register(r"users", AppUserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(def_router.urls))
]
