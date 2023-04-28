""" Los Viewset son colecciones de vistas (list,Creat,Update,Delete), que trabajan con los routers,
los cuales le indican cual utilizar a traves de los métodos http (GET, POST, PUT, PATCH, etc) """

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Colors, Product
from .serializers import (
    ColorsSerializer, ProductSerializer,
    PaginationSerializer, ProductSerializerViewset
)
class ColorViewset(viewsets.ModelViewSet):
    
    serializer_class = ColorsSerializer
    queryset = Colors.objects.all()

class ProductViewset(viewsets.ModelViewSet):
    
    serializer_class = ProductSerializerViewset
    queryset = Product.objects.all()
    pagination_class = PaginationSerializer
    
    def perform_create(self, serializer):
        """ Se utiliza para realizar algun proceso antes del guardado. perfom_create, ya trae
        los datos deserealizados en el atributo serializer """
        print(serializer,'===============')
        serializer.save(
            video = "https://youtu.be/zSmOvYzSeaQ"
        )
    
    def list(self, request, *args, **kwargs):
        """ sobreescribir la manera como se muestran las listas """
        queryset = Product.objects.list_by_user(self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)