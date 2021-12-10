import json

from django.shortcuts import render
from rest_framework import viewsets, status
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.forms.models import model_to_dict
from django.core import serializers

from .constant.ErrorMessages import ErrorMessages
from .constant.JsonKey import JsonKey
from .models import UserProfile, Error, Countries


@csrf_exempt
@api_view(['GET', 'POST'])
def registration(request):
    params = JSONParser().parse(request)
    print(params)
    login = params.get('login')
    password = params.get('password')
    country_id = params.get('country')
    country = Countries.objects.get(id=country_id)
    errors = Error()

    if request.method == 'GET':
        print('GET')
        users = serializers.serialize('json', UserProfile.objects.all())  # UserProfile.objects.all()
        print(users)
        return JsonResponse(users, status=status.HTTP_200_OK, safe=False)

    elif request.method == 'POST':
        print("POST")

        try:
            UserProfile.objects.get(login=login, password=password)
            print("NOT ERROR EXIST")
            # Если есть зареганый аккаунт, то сработает этот сценарий
            errors.append(ErrorMessages.REGISTRATION_ERROR_400)
            return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            pass

        user = UserProfile.objects.create(login=login, password=password, country=country)
        user.save()

        data = {
            JsonKey.UserProfile.ID: user.id,
            JsonKey.UserProfile.LOGIN: user.login,
            JsonKey.UserProfile.PASSWORD: user.password,
            JsonKey.UserProfile.COUNTRY_ID: user.country.id
        }

        return JsonResponse(data, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['POST'])
def login(request):
    params = JSONParser().parse(request)
    print(params)
    login = params.get('login')
    password = params.get('password')
    errors = Error()


    if request.method == 'POST':
        print("POST")

        if (login == None or password == None):
            errors.append(ErrorMessages.NOT_FOUND_REQUIRED_PARAMS)
            return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserProfile.objects.get(login=login, password=password)
            print("NOT ERROR EXIST")
        except UserProfile.DoesNotExist:
            errors.append(ErrorMessages.LOGIN_ERROR_401)
            return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_401_UNAUTHORIZED)

        data = {
            JsonKey.UserProfile.ID: user.id,
            JsonKey.UserProfile.LOGIN: user.login,
            JsonKey.UserProfile.PASSWORD: user.password,
            JsonKey.UserProfile.COUNTRY: {
                JsonKey.Countries.ID: user.country.id,
                JsonKey.Countries.TITLE: user.country.title,
                JsonKey.Countries.PREFIX: user.country.prefix
            }
        }

        return JsonResponse(data, status=status.HTTP_200_OK)
