import string
import random

from django.contrib.auth import authenticate
from django.core.mail import EmailMessage

from rest_framework import generics, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from members.exceptions import EmailSendFailException, UserTokenNotMatchFailException, \
    UserNotExistsException, UserTemporaryPasswordCreateFailException, UserPasswordCheckFailException, \
    UsernameDuplicateFailException
from members.models import User
from members.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from members.text import message, temporary_password_message


class UserList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


### 테스트 코드 통해서 !!!!! 꼭 API 확인하기!!!!!!!!
# Login APIView
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
            # 로그인 실패
            raise AuthenticationFailed()
        # 로그인 성공 && 토큰 생성
        # 더 세밀하게 쪼개서 보내주기
        return Response({'token': token.key,
                         'user': UserSerializer(token.user).data,
                         "detail": "로그인 성공 && 토큰 생성"
                         }, status=status.HTTP_200_OK)


# User Duplicate Check APIView
class UserDuplicateCheckAPIView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        username = request.data['username']
        try:
            # user exists
            user_obj = User.objects.get(username=username)
        except:
            user_obj = None
        if user_obj:
            # 이미 아이디가 존재함
            if user_obj.is_active:

                raise UsernameDuplicateFailException()
            else:
                return Response(
                    data={"detail": "사용 가능합니다"}, status=status.HTTP_200_OK)

        else:
            # 아이디 이메일 존재하지 않는다는 메세지 보내기
            # 가입하면 됨
            return Response(
                data={"detail": "사용 가능합니다"}, status=status.HTTP_200_OK)


# 이메일로 인증 URL 보내는 API
class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            # email 토큰 보내
            try:
                message_data = message('127.0.0.1:8000', user.pk, token)
                mail_title = "Keyword-it 입니다. 이메일 인증을 완료해 주세요"
                mail_to = user.email
                email = EmailMessage(mail_title, message_data, to=[mail_to])
                email.send()
            except:
                return EmailSendFailException()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# email Authenticate APIView
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
            return UserTokenNotMatchFailException()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# maintain user login APIView
class CheckTokenAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key,
                         'user': self.serializer_class(token.user).data}, status=status.HTTP_200_OK)


# user password forget APIView
class UserFindPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        email = request.data['email']
        username = request.data['username']
        try:
            # user exists
            user_obj = User.objects.get(email=email, username=username)
        except:
            user_obj = None
        if user_obj:
            # password make
            password_chars = string.ascii_letters + string.digits + string.punctuation
            length = random.randint(12, 15)

            password = "".join([random.choice(password_chars) for _ in range(length)])
            try:
                user_obj.set_password(password)
                user_obj.save()
            except:
                return UserTemporaryPasswordCreateFailException()
            # email message make
            message_data = temporary_password_message(email, password)
            mail_title = f"Keyword-it 입니다. 임시 비밀번호 발행 메일 입니다."
            mail_to = user_obj.email
            email = EmailMessage(mail_title, message_data, to=[mail_to])
            email.send()
            return Response(status=status.HTTP_200_OK)
        else:
            # 아이디 이메일 존재하지 않는다는 메세지 보내기
            # request 가 잘못된경우의 status 값 보내기
            return UserNotExistsException()


# new password or user infomation update APIView
# 부분 업데이트인가? partial 부분 확인
class UserInfoChangeAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()

    def get_object(self):
        print('APIVIew get_object')
        obj = self.request.user
        # password = self.request.data['password']
        # new_password = self.request.data['newPassword']
        # check_password_value = obj.check_password(password)
        # if check_password_value:
        #     self.request.data['password'] = new_password
        #     print(self.request.data)
        return obj

    # def put(self, request, *args, **kwargs):
    #     print('APIView put method')
    #     return self.partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        print('APIView update method ')
        print(request.data)
        new_password = request.data['newPassword']
        check_password_value = self.request.user.check_password(request.data['password'])
        check_password_last_and_new = request.data['password'] == new_password
        print('check ', check_password_last_and_new)
        if check_password_value and not check_password_last_and_new:
            instance = self.get_object()
            instance.set_password(new_password)
            instance.save()
            # why mobile number exists error
            # even if mobile phone exists and same mobile number just update i want
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            print(serializer.data)
            return Response(serializer.data)
        else:
            # error customize not check password value False
            # or last pw is same with new pw
            return UserPasswordCheckFailException()

    def perform_update(self, serializer):
        print('APIView perform update')
        serializer.save()

    # def partial_update(self, request, *args, **kwargs):
    #     print('APIView ====partial update method')
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)
