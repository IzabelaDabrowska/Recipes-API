from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from categories.views import CategoryViewSet
from recipes.views import RecipeReviewView, RecipeViewSet
from tags.views import TagViewSet
from users.views import (ActivateAccountView, AddRecipeToFavorite,
                         AppUserViewSet, RegisterView, ResendActivationCode)

def_router = DefaultRouter()
def_router.register(r"users", AppUserViewSet)
def_router.register(r"recipes", RecipeViewSet)
def_router.register(r"recipes/(?P<recipe_id>\d+)/reviews", RecipeReviewView)

urlpatterns = (
    [
        path('admin/', admin.site.urls),
        path('api/', include(def_router.urls)),
        path('api/auth/register/', RegisterView.as_view()),
        path('api/auth/resend-code/', ResendActivationCode.as_view()),
        path('api/auth/activate/', ActivateAccountView.as_view()),
        path('api/auth/login/', TokenObtainPairView.as_view()),
        path('api/auth/refresh/', TokenRefreshView.as_view()),
        path('api/add-to-favorite/', AddRecipeToFavorite.as_view()),
        path('api/categories/', CategoryViewSet.as_view()),
        path('api/tags/', TagViewSet.as_view()),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
