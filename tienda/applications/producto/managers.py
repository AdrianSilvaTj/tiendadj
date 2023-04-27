from django.db import models

class ProductManager(models.Manager):
    
    def list_by_user(self, user):
        return self.filter(
            user_created = user
        )
        
    def with_stock_list(self):
        return self.filter(stok__gt=0).order_by('-num_sales')
    
    def by_gender_list(self, genero):
        if genero == 'h':
            mujer = False
            hombre = True
        elif genero == 'm':
            mujer = True
            hombre = False
        else:
            mujer = True
            hombre = True
        return self.filter(
            woman = mujer, man = hombre
        ).order_by('created')
        
    def by_filter_list(self, **filters):
        return self.filter(
            man = filters['man'],
            woman = filters['woman'],
            name__icontains = filters['name']
        )