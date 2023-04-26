from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from firebase_admin import auth

from django.shortcuts import render

from django.views.generic import TemplateView 

from .serializers import LoginSocialSerializer
from .models import User

class LoginUser(TemplateView):
    template_name = 'users/login.html'
    
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