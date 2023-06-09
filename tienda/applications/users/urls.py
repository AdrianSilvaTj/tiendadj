from django.urls import path
from . import views

app_name = 'user_app'
urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('api/google_login/', views.GoogleLoginApiView.as_view(), name='google_login'),
]
