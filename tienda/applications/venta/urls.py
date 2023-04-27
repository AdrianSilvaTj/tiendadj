from django.urls import path
from . import views

app_name = 'sale_app'
urlpatterns = [
    path('api/sale/report/', views.SaleReportListApiView.as_view(), name='report'),
    path('api/sale/register/', views.SaleRegister.as_view(), name='register'),
]