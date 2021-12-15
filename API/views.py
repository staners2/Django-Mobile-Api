
import requests
import datetime
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
import json

from .Helpers import Helpers
from .constant.ApiUrl import ApiUrl
from .constant.ErrorMessages import ErrorMessages
from .constant.JsonKey import JsonKey
from .models import UserProfile, Error, Countries, Histories, Types, Fact


@csrf_exempt
@api_view(['GET', 'POST'])
def registration(request):
    params = JSONParser().parse(request)
    print(params)
    login = params.get('login')
    password = params.get('password')
    country_id = params.get('country_id')

    errors = Error()

    if request.method == 'GET':
        print('GET')
        users = serializers.serialize('json', UserProfile.objects.all())  # UserProfile.objects.all()
        print(users)
        return JsonResponse(users, status=status.HTTP_200_OK, safe=False)

    elif request.method == 'POST':
        print("POST")

        if (login == None or password == None or country_id == None):
            errors.append(ErrorMessages.NOT_FOUND_REQUIRED_PARAMS)
            return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_400_BAD_REQUEST)

        country = Countries.objects.get(id=country_id)

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
            JsonKey.UserProfile.COUNTRY: {
                JsonKey.Countries.ID: user.country.id,
                JsonKey.Countries.TITLE: user.country.title,
                JsonKey.Countries.PREFIX: user.country.prefix
            }
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

@csrf_exempt
@api_view(['GET'])
def get_all_countries(request):
    errors = Error()

    countries = Countries.objects.all()

    data = []
    for item in countries:
        data.append({
            JsonKey.Countries.ID: item.id,
            JsonKey.Countries.TITLE: item.title,
            JsonKey.Countries.PREFIX: item.prefix
        })

    result = json.dumps(data)

    return JsonResponse(result, status=status.HTTP_200_OK, safe=False)

# @csrf_exempt
# @api_view(['GET'])
# def get_country(request, id):
#     country = Countries.objects.get(id=id)
#
#     data = {
#         JsonKey.Countries.ID: country.id,
#         JsonKey.Countries.TITLE: country.title,
#         JsonKey.Countries.PREFIX: country.prefix
#     }
#
#     print(data)
#
#     return JsonResponse(data, status=status.HTTP_200_OK, safe=False)

@csrf_exempt
@api_view(['PUT'])
def update_country(request, userprofile_id):
    params = JSONParser().parse(request)
    print(params)
    country_id = params.get(JsonKey.Countries.ID)
    errors = Error()

    if (country_id == None):
        errors.append(ErrorMessages.NOT_FOUND_REQUIRED_PARAMS)
        return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_400_BAD_REQUEST)

    try:
        country = Countries.objects.get(id=country_id)
        print("NOT ERROR EXIST")
    except Countries.DoesNotExist:
        errors.append(ErrorMessages.COUNTRIES_NOT_FOUND)
        return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_404_NOT_FOUND)


    user = UserProfile.objects.get(id=userprofile_id)
    user.country = country
    user.save()

    data = {
        JsonKey.UserProfile.ID: user.id,
        JsonKey.UserProfile.LOGIN: user.login,
        JsonKey.UserProfile.PASSWORD: user.password,
        JsonKey.UserProfile.COUNTRY: {
            JsonKey.Countries.ID: user.country.id,
            JsonKey.Countries.TITLE: Helpers.translate_language("en", country.prefix, user.country.title),
            JsonKey.Countries.PREFIX: user.country.prefix
        }
    }

    return JsonResponse(data, status=status.HTTP_200_OK, safe=False)

@csrf_exempt
@api_view(['GET'])
def show_histories(request, userprofile_id):
    user = UserProfile.objects.get(id = userprofile_id)
    histories = Histories.objects.filter(user = user)
    errors = Error()

    if len(histories) == 0:
        errors.append(ErrorMessages.HISTORIES_NOT_FOUND)
        return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_200_OK)

    print(histories)
    data = []


    for item in histories:
        data.append({
        JsonKey.Histories.ID: item.id,
        JsonKey.Histories.DATE: item.date.strftime("%Y-%m-%d %H:%M:%S"),
        JsonKey.Histories.DESCRIPTION: Helpers.translate_language("en", user.country.prefix, item.description),
        JsonKey.Histories.USER: {
            JsonKey.UserProfile.ID: item.user.id,
            JsonKey.UserProfile.LOGIN: item.user.login,
            JsonKey.UserProfile.PASSWORD: item.user.password,
            JsonKey.UserProfile.COUNTRY: {
                JsonKey.Countries.ID: item.user.country.id,
                JsonKey.Countries.TITLE: Helpers.translate_language("en", user.country.prefix, item.user.country.title),
                JsonKey.Countries.PREFIX: item.user.country.prefix
            }
        },
        JsonKey.Histories.TYPE: {
            JsonKey.Types.ID: item.type.id,
            JsonKey.Types.RU_TITLE: Helpers.translate_language("ru", user.country.prefix, item.type.ru_title),
            JsonKey.Types.EN_TITLE: item.type.en_title
        }
    })

    result = json.dumps(data)
    print(result)

    return JsonResponse(result, status=status.HTTP_200_OK, safe=False)

@csrf_exempt
@api_view(['DELETE'])
def delete_histories(request, userprofile_id, history_id):
    user = UserProfile.objects.get(id=userprofile_id)
    errors = Error()

    try:
        history = Histories.objects.get(user=user, id = history_id)
        print("NOT ERROR EXIST")
    except Histories.DoesNotExist:
        errors.append(ErrorMessages.HISTORY_NOT_FOUND)
        return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_404_NOT_FOUND)

    history.delete()

    return HttpResponse(status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
def get_random_fact(request, type):
    errors = Error()

    params = JSONParser().parse(request)

    userprofile_id = params.get("userprofile_id")

    headers = {
        "Content-Type": "application/json"
    }

    if (type == None or len(Types.objects.filter(en_title = type)) == 0):
        errors.append(ErrorMessages.GET_RANDOM_TYPES_NOT_FOUND)
        return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_404_NOT_FOUND)

    if (userprofile_id == None):
        errors.append(ErrorMessages.NOT_FOUND_REQUIRED_PARAMS)
        return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_404_NOT_FOUND)

    user = UserProfile.objects.get(id=userprofile_id)

    urlList = {
        'trivia': ApiUrl.RANDOM_TRIVIA,
        'year': ApiUrl.RANDOM_YEAR,
        'date': ApiUrl.RANDOM_DATE,
        'math': ApiUrl.RANDOM_MATH,
    }

    response = requests.get(headers=headers, url=urlList[type])
    print(response.text)
    obj = json.loads(response.text)

    type = Types.objects.get(en_title=obj["type"])
    fact = Fact(number=obj["number"], text=obj["text"], type=type)

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history = Histories.objects.create(user=user, type=type, date=date, number=fact.number, description=fact.text)
    history.save()

    data = {
        JsonKey.Fact.NUMBER: history.number,
        JsonKey.Fact.TEXT: Helpers.translate_language("en", user.country.prefix, history.description),
        JsonKey.Fact.TYPE: {
            JsonKey.Types.ID: type.id,
            JsonKey.Types.RU_TITLE: Helpers.translate_language("ru", user.country.prefix, type.ru_title),
            JsonKey.Types.EN_TITLE: type.en_title
        }
    }

    return JsonResponse(data, status=status.HTTP_200_OK, safe=False)

@csrf_exempt
@api_view(['GET'])
def get_fact_by_type(request, type, number):
    errors = Error()

    params = JSONParser().parse(request)

    userprofile_id = params.get("userprofile_id")

    headers = {
        "Content-Type": "application/json"
    }

    if (type == None or len(Types.objects.filter(en_title=type)) == 0):
        errors.append(ErrorMessages.GET_RANDOM_TYPES_NOT_FOUND)
        return JsonResponse({JsonKey.ERRORS: errors.messages}, status=status.HTTP_404_NOT_FOUND)

    user = UserProfile.objects.get(id=userprofile_id)

    url=ApiUrl.GENERATE_URL_BY_NUMBER_AND_TYPE.format(number, type)

    response = requests.get(headers=headers, url=url)
    print(response.text)
    obj = json.loads(response.text)

    type = Types.objects.get(en_title=obj["type"])
    fact = Fact(number=obj["number"], text=obj["text"], type=type)

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history = Histories.objects.create(user=user, type=type, date=date, number=fact.number, description=fact.text)
    history.save()

    data = {
        JsonKey.Fact.NUMBER: fact.number,
        JsonKey.Fact.TEXT: Helpers.translate_language("en", user.country.prefix, history.description),
        JsonKey.Fact.TYPE: {
            JsonKey.Types.ID: type.id,
            JsonKey.Types.RU_TITLE: Helpers.translate_language("ru", user.country.prefix, type.ru_title),
            JsonKey.Types.EN_TITLE: type.en_title
        }
    }

    return JsonResponse(data, status=status.HTTP_200_OK, safe=False)