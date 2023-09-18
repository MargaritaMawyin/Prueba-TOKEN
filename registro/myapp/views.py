from typing import Any
from django import http
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework import viewsets
from .serializer import TokenSerializer
from .models import Token, ManejoDeToken
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import random
from datetime import datetime, timedelta

# Create your views here.


class TokenView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # def get(self, request, id=0):
    #     if (id>0):
    #         registros=list(Token.objects.filter(id=id).values())
    #         if len(registros) >0:
    #             reg = registros[0]
    #             datos = {"message": "Success", "registro": reg}
    #         else:
    #             datos = {"message": "No encontrado..."}
    #         return JsonResponse(datos)
    #     else:
    #         registros = list(Token.objects.values())
    #         if len(registros) > 0:
    #             datos = {"message": "Success", "registros": registros}
    #         else:
    #             datos = {"message": "No encontrado..."}
    #         return JsonResponse(datos)


    def get(self, request, usuario=''):
        if usuario:
            registros = list(Token.objects.filter(usuario=usuario).values())
            if len(registros) > 0:
                datos = {"message": "Success", "registros": registros}
            else:
                datos = {"message": "No encontrado para el usuario especificado..."}
            return JsonResponse(datos)
        else:
            registros = list(Token.objects.values())
            if len(registros) > 0:
                datos = {"message": "Success", "registros": registros}
            else:
                datos = {"message": "No encontrado..."}
            return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        Token.objects.create(token=jd['token'], usuario=jd['usuario'])
        datos = {"message": "Success"}
        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        registros = list(Token.objects.values())
        if len(registros) > 0:
            registros = Token.objects.get(id=id)
            registros.token = jd['token']
            registros.usuario = jd['usuario']
            registros.save()
            datos = {"message": "Success"}
        else:
            datos = {"message": "No encontrado..."}
        return JsonResponse(datos)

    def delete(self, request, id):
        registro = list(Token.objects.filter(id=id).values())
        if len(registro) > 0:
            Token.objects.filter(id=id).delete()
            datos = {"message": "Success"}

        else:
            datos = {"message": "No encontrado..."}
        return JsonResponse(datos)


# Desactiva la protección CSRF para simplificar el ejemplo (no lo hagas en producción sin protección CSRF)
@csrf_exempt
def generar_token(request):
    usuario = request.GET.get('usuario')
    # Verificar si ya existe un token válido para el usuario
    tokens_existentes = Token.objects.filter(
        usuario=usuario, expiracion__gt=datetime.now())
    if tokens_existentes.exists():
        # Si existe un token válido, devolver ese token con el tiempo restante
        token = tokens_existentes.first()
        tiempo_restante = (token.expiracion - datetime.now()).total_seconds()
        return JsonResponse({'token': token.token, 'tiempo_restante': tiempo_restante})
    # Generar un nuevo token de 6 dígitos
    nuevo_token = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    # Calcular la hora de expiración (60 segundos desde ahora)
    hora_expiracion = datetime.now() + timedelta(seconds=60)

    # Guardar el nuevo token en la base de datos
    Token.objects.create(usuario=usuario,
                         token=nuevo_token,
                         expiracion=hora_expiracion)

    return JsonResponse({'token': nuevo_token, 'tiempo_restante': 60})


# Desactiva la protección CSRF para simplificar el ejemplo (no lo hagas en producción sin protección CSRF)
@csrf_exempt
def usar_token(request):
    usuario = request.GET.get('usuario')
    token_token = request.GET.get('token')

    # Buscar el token en la base de datos
    token = Token.objects.filter(
        usuario=usuario, token=token_token, expiracion__gt=datetime.now()).first()

    if token:
        return JsonResponse({'mensaje': 'Token válido'})
    else:
        return JsonResponse({'mensaje': 'Token no válido o caducado'})


def generar_token_endpoint(request):
    if request.method == 'POST':
        # Genera un nuevo token llamando a la función generar_token
        token = generar_token(request)
        return JsonResponse({'token': token})
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

  # Desactiva la protección CSRF para simplificar el ejemplo (no lo hagas en producción sin protección CSRF)


def usar_token_endpoint(request):
    if request.method == 'POST':
        # Obtiene el token de la solicitud (deberías enviarlo en el cuerpo de la solicitud)
        token = request.POST.get('token', '')
        # Utiliza el token llamando a la función usar_token
        resultado = usar_token(token)
        if resultado:
            return JsonResponse({'message': 'Token válido'})
        else:
            return JsonResponse({'message': 'Token inválido'}, status=400)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)


class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer

# def token(request):
#     tokens = Token.objects.all()
#     return render(request, 'base.html', {"token": tokens})
