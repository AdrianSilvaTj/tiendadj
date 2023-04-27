from django.urls import path
from . import views

app_name = 'product_app'
urlpatterns = [
    path('api/product/by_user/', views.ProductUserListApiView.as_view(), name='by_user'),
    path('api/product/with_stock/', views.WithStockListApiView.as_view(), name='with_stock'),
    path('api/product/by_gender/<gend>', views.ByGenderListApiView.as_view(), name='by_gender'),
    path('api/product/by_filter/', views.ByFilterListApiView.as_view(), name='by_filter'),
]
