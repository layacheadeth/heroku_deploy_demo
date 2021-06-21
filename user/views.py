import jwt
from django.shortcuts import render
from .serializer import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
import datetime
import jwt

class RegisterView_with_condition(APIView):
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        first_name=request.data['first_name']
        last_name = request.data['last_name']

        if User.objects.filter(email=email).exists():
            print("Email is already taken")
            print("Account has been created using this email")
        else:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)



class RegisterView(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self,request):
        username=request.data['username']
        password=request.data['password']

        user=User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        # get the user.id, validate for how long this user can login using this token
        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow(),
        }
        # create token using jwt and base on hash algorithm
        token=jwt.encode(payload,'secret',algorithm='HS256')
        response=Response()
        # set cookie for this token, only send to the backend at the time cookie is being generated.
        # after cookie is being generated, it will be access and use by frontend.
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={
            'jwt':token,
        }
        return response


class UserView(APIView):
    def get(self,request):
        # get the cookie from frontend to allow access, cookie is preserved.
        # the cookie we get refer to the user who log into our website.
        # we will receive our user log in as a result if the cookie is refering to the logged in person.
        token=request.COOKIES.get('jwt')
        # if false, Unauthenticated mean this user has not been granted permisson to log in.
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        # if not false, then refer the cookie to the correspond data, then decode it and show the data
        # as a result, we got info of login user since we return the first or recent login user data which will be then serialize to json format.
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user=User.objects.filter(id=payload['id']).first()
        serializer=UserSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    # delete cookie when logout. Thus, when login again, use new cookie.
    def post(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            'message':'success',
        }
        return response








