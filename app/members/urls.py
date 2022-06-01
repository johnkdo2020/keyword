from django.urls import path

from members.apis import UserList, UserCreateAPIView, AuthTokenAPIView, UserAuthenticatedAPIView, UserInfoChangeAPIView, \
    CheckTokenAPIView, UserFindPasswordAPIView, UserDuplicateCheckAPIView

app_name = 'members'
urlpatterns = [
    path('', UserList.as_view(), name="user-list"),
    path('login/', AuthTokenAPIView.as_view(), name="user-login"),
    path('sign/', UserCreateAPIView.as_view(), name="user-create"),
    path('active/<int:pk>/<str:token>/', UserAuthenticatedAPIView.as_view(), name="user-authenticated"),
    path('change/', UserInfoChangeAPIView.as_view(), name="user-change"),
    path('check/', CheckTokenAPIView.as_view(), name="user-check"),
    path('password/', UserFindPasswordAPIView.as_view(), name='user-forget-password]'),
    path('duplicate/', UserDuplicateCheckAPIView.as_view(), name='username-check'),

]
