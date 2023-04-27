from django.db import models

class SailDetailManager(models.Manager):
    
    def products_by_sale(self, saleId):
        query = self.filter(sale__id = saleId).order_by('count', 'product__name')
        return query