from django.utils import timezone

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView, CreateAPIView
)

from applications.producto.models import Product
from .models import Sale, SaleDetail
from .serializers import (
    SaleReportSerializer, SaleProcessSerializer, SaleProcessSerializer2
)

class SaleReportListApiView(ListAPIView):
    serializer_class = SaleReportSerializer
    
    def get_queryset(self):
        return Sale.objects.all()
    
class SaleRegister(CreateAPIView):
    """ Registra una nueva venta """
    serializer_class = SaleProcessSerializer
    authentication_classes = (TokenAuthentication,) # Para autenticar el Token
    permission_classes = [IsAuthenticated] # Solo permite acceder si esta autenticado

    def create(self, request, *args, **kwargs):
        """ Este metodo se ejecuta una vez que se ha hecho post desde el frontend """
        # Deserializamos la información que nos envían desde el json
        szer_data = SaleProcessSerializer( data= request.data )
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
        arrproducts = []
        arrproducts = szer_data.validated_data['products']
        print(arrproducts)
        # Creamos un array de registros de de los productos de la venta para registrarlos en el
        # modelo SaleDetail
        arr_sale_detail = []
        # recorremos o iteramos la lista de productos        
        for pro in arrproducts:
            # (B) obtenemos el objeto del producto atraves del id
            product = Product.objects.get(id = pro['id'])
            # creamos un registro de venta detalle
            sale_detail = SaleDetail(
                sale = sale, # objeto sale que acabado de crear arriba (A)
                product = product, # objeto que obtuvimos (B)
                count = pro['count'],
                price_purchase = product.price_purchase,
                price_sale = product.price_sale,
            )
            # Calculamos el monto de la venta y la cantidad de productos
            calc_amount = calc_amount + (product.price_sale * pro['count'])
            calc_count = calc_count + pro['count']
            # agregamos ese registro al arreglo
            arr_sale_detail.append(sale_detail)            
        # Registramos en lote
        SaleDetail.objects.bulk_create(arr_sale_detail)
        #Actualizamos los campos amount y count de la venta
        sale.amount = calc_amount
        sale.count = calc_count        
        sale.save()        
        
        return Response({ 'msj ': 'Venta Exitosa'})
    
class SaleRegister2(CreateAPIView):
    """ Registra una nueva venta utilizando el serializers.ListField """
    serializer_class = SaleProcessSerializer2
    authentication_classes = (TokenAuthentication,) # Para autenticar el Token
    permission_classes = [IsAuthenticated] # Solo permite acceder si esta autenticado

    def create(self, request, *args, **kwargs):
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
        
        return Response({ 'msj ': 'Venta Exitosa'})