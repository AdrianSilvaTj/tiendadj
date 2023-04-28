from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .models import Sale, SaleDetail, Product
from .serializers import (
   SaleProcessSerializer2, SaleReportSerializer
)

class SaleViewSet(viewsets.ViewSet):
    """ Este viewset no esta casado con ningún Model, una desventaja es que a la hora
    de algun error solo nos mandara un error 404.
        En viewsets.ViewSet, se deben redefinir todos los metodos para que sepa que hacer
    """
    authentication_classes = (TokenAuthentication,) # Para autenticar el Token
    # permission_classes = [IsAuthenticated] # Solo permite acceder si esta autenticado
    
    def get_permissions(self):
        """ asignamos el tipo de permiso que va a tener cada uno de los metodos(action) """
        if (self.action == 'list') or (self.action == 'retrieve'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]        
        return [permission() for permission in permission_classes]
    
    def list(self, request):
        queryset =  Sale.objects.all()
        serializer = SaleReportSerializer(queryset, many=True)        
        return Response(serializer.data)
    
    def create (self, request):
        """ Este metodo se ejecuta una vez que se ha hecho post desde el frontend """
        # Deserializamos la información que nos envían desde el json
        szer_data = SaleProcessSerializer2( data= request.data )
        # Verificamos que el json tenga todo los datos con el formato correcto
        szer_data.is_valid(raise_exception=True)
        # (A) Recuperamos la información de los campos como un diccionario y creamos la venta
        sale = Sale.objects.create(
            date_sale = timezone.now(),
            amount = 0,
            count = 0,
            type_invoce = szer_data.validated_data['type_invoce'],
            type_payment = szer_data.validated_data['type_payment'],
            adreese_send = szer_data.validated_data['adreese_send'],
            user = self.request.user
        )
        calc_amount = 0
        calc_count = 0
        # Recuperamos los productos de la venta (es un array)
        # id__in, busca todos los productos con los id recibidos y los retorna en un array
        arrproducts = Product.objects.filter(
            id__in = szer_data.validated_data['products']
        )
        arrcounts = szer_data.validated_data['counts']
        # Creamos un array de registros de de los productos de la venta para registrarlos en el
        # modelo SaleDetail
        arr_sale_detail = []
        # recorremos o iteramos la lista de productos y de cantidades al mismo tiempo       
        for product, count in zip(arrproducts, arrcounts):            
            # creamos un registro de venta detalle
            sale_detail = SaleDetail(
                sale = sale, # objeto sale que acabado de crear arriba (A)
                product = product,
                count = count,
                price_purchase = product.price_purchase,
                price_sale = product.price_sale,
            )
            # Calculamos el monto de la venta y la cantidad de productos         
            calc_amount = calc_amount + (product.price_sale * count)
            calc_count = calc_count + count
            # agregamos ese registro al arreglo
            arr_sale_detail.append(sale_detail)            
        # Registramos en lote
        SaleDetail.objects.bulk_create(arr_sale_detail)
        #Actualizamos los campos amount y count de la venta
        sale.amount = calc_amount
        sale.count = calc_count        
        sale.save()
        # Creo el Json de respuesta, con el objeto creado y le agrego un campo result, con el resultado
        # de la operación
        json_rensp = SaleReportSerializer(sale).data
        json_rensp['result'] = 'susccesfully'        
        return Response(json_rensp)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Sale.objects.all(), pk=pk)
        serializer = SaleReportSerializer(queryset)
        return Response(serializer.data)