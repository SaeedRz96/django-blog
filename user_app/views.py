import datetime
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from .authentication import create_access_token, JWTAuthentication, create_refresh_token, decode_refresh_token
from django.contrib.auth.models import User
from .serializers import UserSerializer
from user_app.models import UserToken


class CheckUserExistsAPIView(APIView):
    """
    This view checks if a user exists in the database.
    requeste data: 
        username[string]: mandatory
    response: 
        200 if user exists, 404 if user does not exist
    """
    def post(self, request):
        data = request.data
        if User.objects.filter(username=data['username']).exists():
            return Response(status=200, data={'message': 'user exists'})
        else:
            return Response(status=404, data={'message': 'user does not exist'})


class RegisterAPIView(APIView):
    """
    This view registers a user in the database.
    request data:
        first_name[string]: mandatory
        last_name[string]: mandatory
        username[string]: mandatory
        password[string]: mandatory
        password_confirm[string]: mandatory
    response:
        registered user info if user is registered successfully, 400 if user is not registered successfully
    """
    def post(self, request):
        data = request.data
        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match!')
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class LoginAPIView(APIView):
    """
    This view logs in a user.
    request data:
        username[string]: mandatory
        password[string]: mandatory
    response:
        access_token
    """
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username=username).first()
        if user is None:
            raise exceptions.AuthenticationFailed('Invalid username')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Invalid password')
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        UserToken.objects.create(
            user_id = user.id,
            token = refresh_token,
            expired_at = datetime.datetime.now() + datetime.timedelta(days=7)
        )
        response = Response()
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.data = {
            'token': access_token
        }
        return response


class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    """
    This view returns the user info as verified by the JWTAuthentication class.
    request data: 
        none 
        (only the access token is required)
    response:
        user info
    """
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class RefreshAPIView(APIView):
    """
    This view refreshes the access token.
    request data:
        none
        (only the refresh token is required)
    response:
        new access token
    """
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)
        if not UserToken.objects.filter(
                user_id=id,
                token=refresh_token,
                expired_at__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).exists():
            raise exceptions.AuthenticationFailed('unauthenticated')
        access_token = create_access_token(id)
        return Response({
            'token': access_token
        })


class LogoutAPIView(APIView):
    """
    This view logs out a user.
    request data:
        none
        (only the refresh token is required)
    response:
        success message with status 200
    """
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        UserToken.objects.filter(token=refresh_token).delete()

        response = Response()
        response.delete_cookie(key='refresh_token')
        response.data = {
            'message': 'user logged out successfully'
        }

        return response