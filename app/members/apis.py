from django.contrib.auth import authenticate
from django.core.mail import EmailMessage

from rest_framework import generics, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from members.models import User
from members.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from members.text import message


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthTokenAPIView(APIView):
    """
        사용자가 인증되면 token 값을 보내주는 api
    """
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        print(email, password)
        user = authenticate(email=email, password=password)
        print(user)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
        else:
            raise AuthenticationFailed()

        return Response({'token': token.key,
                         'user': UserSerializer(token.user).data})


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            # email 토큰 보내
            message_data = message('127.0.0.1:8000', user.pk, token)
            mail_title = "이메일 인증을 완료해 주세요"
            mail_to = user.email
            email = EmailMessage(mail_title, message_data, to=[mail_to])
            email.send()
            return Response(status=status.HTTP_201_CREATED)
        else:
            print('fail')
            return Response(data=serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class UserAuthenticatedAPIView(generics.RetrieveAPIView):
    # authenticated api and change user is_active = True
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        user = self.queryset.get(pk=self.kwargs.get("pk"))
        token = get_object_or_404(Token, pk=self.kwargs.get("token"))
        if token.user == user:
            user.is_active = True
            user.save()
            # obj = get_object_or_404(Member, pk=self.kwargs.get("pk"))
            return user
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UserInfoChangeAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()

    def get_object(self):
        new_password = self.request.data['newPassword']
        obj = self.request.user
        obj.set_password(new_password)
        obj.save()
        return obj

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CheckTokenAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key,
                         'user': self.serializer_class(token.user).data})
