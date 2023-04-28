""" De esta manera se manejan las urls cuando se trabaja con viewsets con los routers,
estos le indican al viewset que vista utilizar de acuerdo al metodo http (GET, POST, PUT, PATCH, etc)
que se le envie a traves de la petición"""

""" Para el GET y el POST basta con escribir 'api/colors' para que detecte que vista debe realizar
    Para el PUT, PATCH, DELETE se debe colocar el id: 'api/colors/1'  """
from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()

# Registramos url para nuestro viewset: 
# "r'colors"-> nombre url, 
# "viewsets.ColorViewset" -> viewset,
# "basename="colors"" -> nombre de referencia (similar al name en path)
router.register(r'api/sale', viewsets.SaleViewSet, basename="sale")

# Para poder registrar las rutas en las urls principal
urlpatterns = router.urls