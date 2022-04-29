import string
import random

from django.contrib.auth import authenticate
from django.core.mail import EmailMessage

from rest_framework import generics, status, permissions, mixins
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from members.models import User
from members.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from members.text import message, temporary_password_message


class UserList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny, ]
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
        user = authenticate(email=email, password=password)
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
            mail_title = "Keyword-it 입니다. 이메일 인증을 완료해 주세요"
            mail_to = user.email
            email = EmailMessage(mail_title, message_data, to=[mail_to])
            email.send()
            return Response(status=status.HTTP_201_CREATED)
        else:
            print('UserCreateAPIView fail')
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


class UserFindPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny, ]
    def post(self, request):
        email = request.data['email']
        username = request.data['username']
        try:
            user_obj = User.objects.get(email=email, username=username)
        except:
            user_obj = None
        if user_obj:
            password_chars = string.ascii_letters + string.digits + string.punctuation
            length = random.randint(12, 15)

            password = "".join([random.choice(password_chars) for _ in range(length)])
            print('password', password)
            user_obj.set_password(password)
            user_obj.save()

            message_data = temporary_password_message(email, password)
            mail_title = f"Keyword-it 입니다. 임시 비밀번호 발행 메일 입니다."
            mail_to = user_obj.email
            email = EmailMessage(mail_title, message_data, to=[mail_to])
            email.send()
            return Response(status=status.HTTP_200_OK)
        else:
            # 아이디 이메일 존재하지 않는다는 메세지 보내기
            # request 가 잘못된경우의 status 값 보내기
            return Response(status=status.HTTP_401_UNAUTHORIZED)
