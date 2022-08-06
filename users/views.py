from rest_framework.exceptions import AuthenticationFailed
from urllib import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer
from .models import User
import jwt,datetime

class RegisterView(APIView):
    """
    API to register a user
    """

    def post(self,request,format = None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    API for logging the user
    """

    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found!")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.utcnow() 
        }

        token = jwt.encode(payload,'secret',algorithm='HS256') #.decode('utf-8')

        response = Response()

        response.set_cookie(key = 'jwt', value = token, httponly = True)
        response.data = {
            'jwt' : token
        }

        return response

class UserView(APIView):

    def get(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer  = UserSerializer(user)

        return Response(serializer.data)

class LogoutView(APIView):
    
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message" : "success"
        }
        return response