from rest_framework.generics import (
    ListAPIView
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.shortcuts import render

from .models import Product
from .serializers import ProductSerializer

class ProductUserListApiView(ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,) # Para autenticar el Token
    permission_classes = [IsAuthenticated] # Solo permite acceder si esta autenticado
    
    def get_queryset(self):
        # Recuperar usuario autenticado
        user = self.request.user
        print (user)
        return Product.objects.list_by_user(user)

class WithStockListApiView(ListAPIView):
    """ Listar Productos con Stock """
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,) # Para autenticar el Token
    permission_classes = [IsAuthenticated ,IsAdminUser] # Solo permite acceder si esta autenticado
    
    def get_queryset(self):       
        return Product.objects.with_stock_list()

class ByGenderListApiView(ListAPIView):
    """ Listar Productos Por Genero """
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        # recuperar parametro enviado por url
        gender = self.kwargs['gend']       
        return Product.objects.by_gender_list(gender)

class ByFilterListApiView(ListAPIView):
    """ Listar Productos Por Filtros """
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        # recuperar parametros enviado por metodo GET
        man = self.request.query_params.get('man', None)       
        woman = self.request.query_params.get('women', None)       
        name = self.request.query_params.get('name', None)
        
        return Product.objects.by_filter_list(
            man = man,
            woman = woman,
            name = name
        )