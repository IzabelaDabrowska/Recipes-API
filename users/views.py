from django.http.response import HttpResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import AppUser
from .permissions import BasePermission
from .serializers import (ActivateAccountSerializer,
                          AddRecipeToFavoriteSerializer, AppUserSerializer,
                          RegisterSerializer, ResendActivationCodeSerializer)


class AppUserViewSet(ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    permission_classes = [BasePermission]


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer


class ActivateAccountView(APIView):
    def post(self, request):
        serializer = ActivateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        activation_code = serializer.validated_data["activation_code"]
        email = serializer.validated_data["email"]
        user: AppUser = AppUser.objects.filter(email=email).first()
        if user is None:
            raise Exception('There is no user with provided email')
        user.activate(activation_code)
        return HttpResponse(status=202)


class ResendActivationCode(APIView):
    def post(self, request):
        serializer = ResendActivationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user: AppUser = AppUser.objects.filter(email=email).first()
        if user is None:
            raise Exception('There is no user with provided email')
        user.resend_activation_code()
        return HttpResponse(status=202)


class AddRecipeToFavorite(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddRecipeToFavoriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        recipe = serializer.validated_data["recipe"]

        if user.favorites_recipes.filter(pk=recipe.pk).exists():
            user.favorites_recipes.remove(recipe)
            user.save()
            return Response({"message": "Recipe removed from favorites"}, status=status.HTTP_200_OK)

        user.favorites_recipes.add(recipe)
        user.save()
        return Response({"message": "Recipe added to favorites"}, status=status.HTTP_200_OK)
