from typing import Any
from django import http
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework import viewsets
from .serializer import TokenSerializer
from .models import Token
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.



class TokenView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        registros = list(Token.objects.values())
        if len(registros)>0:
            datos ={"message":"Success", "registros": registros}
        else:
            datos ={"message":"No encontrado..."}
        return JsonResponse(datos)
    

    def post(self, request):
        jd = json.loads(request.body)
        Token.objects.create(token =jd['token'], usuario=jd['usuario'])
        datos ={"message":"Success"}
        return JsonResponse(datos)


    def put(self, request,id):
        jd = json.loads(request.body)
        registros = list(Token.objects.values())
        if len(registros)>0:
            registros=Token.objects.get(id=id)
            registros.token=jd['token']
            registros.usuario=jd['usuario']
            registros.save()
            datos ={"message":"Success"}
        else:
            datos ={"message":"No encontrado..."}
        return JsonResponse(datos)   
    
    def delete(self, request,id):
        registro = list(Token.objects.filter(id=id).values())
        if len(registro) >0:
            Token.objects.filter(id=id).delete()
            datos ={"message":"Success"}

        else:
            datos ={"message":"No encontrado..."}
        return JsonResponse(datos)



class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer

# def token(request):
#     tokens = Token.objects.all()
#     return render(request, 'base.html', {"token": tokens})

