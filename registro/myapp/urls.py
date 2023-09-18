from django.urls import path, include
from rest_framework import routers
from . import views
from .views import TokenView



router = routers.DefaultRouter()
router.register('registro', views.TokenViewSet)

urlpatterns =[
    # path('', include(router.urls)),
    # path("token/", views.Token, name="Token")
    path("token/", TokenView.as_view(), name="Token"),
    path("token/<int:id>", TokenView.as_view(), name="TokenPorId"),
    path("token/<str:usuario>", TokenView.as_view(), name="TokenPorUsuario"),
    path('generarToken/', views.generar_token_endpoint, name='generar_token'),
    path('usarToken/', views.usar_token_endpoint, name='usar_token'),
]
