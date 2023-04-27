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
        print(query[0].id)
        return query_serz
    
class ProductSaleDetailSerializer(serializers.ModelSerializer):
    """ Serializador para el queryset resultante de los productos de la venta """
    class Meta:
        model = SaleDetail
        fields = (
            '__all__'
        )
        
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
    
