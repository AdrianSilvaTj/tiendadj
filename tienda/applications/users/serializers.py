from rest_framework import serializers

class LoginSocialSerializer(serializers.Serializer):
    """ Trabajara con el token de usuario """
    token_id = serializers.CharField(required=True)