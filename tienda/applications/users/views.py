from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from firebase_admin import auth

from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView, View

from .serializers import LoginSocialSerializer
from .models import User

class LoginUser(TemplateView):
    template_name = 'users/login.html'
    
# class LoginUser(FormView):
#     template_name = 'users/login.html'
#     form_class = LoginForm
#     success_url = reverse_lazy('home_app:index')

#     def form_valid(self, form):
#         user = authenticate(
#             email=form.cleaned_data['email'],
#             password=form.cleaned_data['password']
#         )
#         login(self.request, user)
#         return super(LoginUser, self).form_valid(form)


class LogoutView(View):

    def get(self, request, *args, **kargs):
        logout(request)
        print ("********************Logout")
        return HttpResponseRedirect(
            reverse(
                'user_app:login'
            )
        )
    
class GoogleLoginApiView(APIView):
    
    serializer_class = LoginSocialSerializer
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # si es valido, sino la misma funcion retorna el error al poner (raise_exception=True)
        print("*********************************")
        id_token = serializer.data.get('token_id')
        print("/////////////////////////////")
        # decodificar el token
        decoded_token = auth.verify_id_token(id_token)
        print("===================================")
        email = decoded_token['email']
        name = decoded_token['name']
        avatar = decoded_token['picture']
        verified = decoded_token['email_verified']
        # Verifica si existe el usuario, sino, lo crea
        user_ver, created = User.objects.get_or_create(
            email=email,
            defaults={
                'full_name': name,
                'email': email,
                'is_active': True
            }
        )
        # Le asignamos nuestro propio token
        if created:
            token = Token.objects.create(user=user_ver)
        else:
            token = Token.objects.get(user=user_ver)
        print("================",created)
        # Usuario que se devolvera al frontend
        user_get = {
            'id' : user_ver.id,
            'email' : user_ver.email,
            'full_name' : user_ver.full_name,
            'genero' : user_ver.genero,
            'date_birth' : user_ver.date_birth,
            'city' : user_ver.city
        }
        # Devolver un diccionario    
        return Response(
            {
                'token' : token.key,
                'user' : user_get
            }
        )