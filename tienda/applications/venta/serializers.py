from rest_framework import serializers

from .models import Sale, SaleDetail

class SaleReportSerializer(serializers.ModelSerializer):
    """ Serializador para ver las ventas con su detalle """
    # Sera un objeto jason resultado del filtro
    product = serializers.SerializerMethodField()
    
    class Meta:
        model = Sale
        fields = (
            'id',
            'date_sale',
            'amount',
            'count',
            'type_invoce',
            'cancelado',
            'type_payment',
            'state',
            'adreese_send',
            'user',
            'product'
        )
        
    def get_product(self, obj):
        """ Agregamos los valores del campo 'product' """
        # Obtenemos en el manager los detalles de esa venta
        query = SaleDetail.objects.products_by_sale(obj.id)
        # Serializamos el queryset obtenido, y obtenemos sus datos a traves de .data
        query_serz = ProductSaleDetailSerializer(query, many=True).data
        return query_serz
    
class ProductSaleDetailSerializer(serializers.ModelSerializer):
    """ Serializador para el queryset resultante de los productos de la venta """
    class Meta:
        model = SaleDetail
        fields = (
            '__all__'
        )

""" JSon para recibir la información en este serializador (SaleProcessSerializer) :
{
    "type_invoce":"0",
    "type_payment":"0",
    "adreese_send":"Calle Prueba Barrio Prueba",
    "products": [{"id":1, "count":2},{"id":5, "count":4}]
}
"""    
class SaleProductDetailSerializer(serializers.Serializer): 
    """ Serializador para los productos dentro de la venta """   
    id = serializers.IntegerField()
    count = serializers.IntegerField()
        
class SaleProcessSerializer(serializers.Serializer):
    """ Serializador para un proceso de venta """
    type_invoce = serializers.CharField()
    type_payment = serializers.CharField()
    adreese_send = serializers.CharField()
    products = SaleProductDetailSerializer(many=True)

""" JSon para recibir la información en este serializador (SaleProcessSerializer2) :
{
    "type_invoce":"0",
    "type_payment":"0",
    "adreese_send":"Calle Prueba Barrio Prueba",
    "products": [1,2,3],
    "counts" : [10,25,8]
}
"""  
class ArrayIntegerSerializer(serializers.ListField):
    """ Serializador para trabajar con un arreglo de enteros """
    child = serializers.IntegerField()
    
class SaleProcessSerializer2(serializers.Serializer):
    """ Serializador para un proceso de venta """
    type_invoce = serializers.CharField()
    type_payment = serializers.CharField()
    adreese_send = serializers.CharField()
    products = ArrayIntegerSerializer()
    counts = ArrayIntegerSerializer()

    
    
    def validate_type_invoce(self, value):
        print("******************")
        print(Sale.validate_)
        print (value)
        if value not in Sale.TIPO_INVOCE :
            raise serializers.ValidationError('Ingrese un valor correcto')
        return value
    
    
