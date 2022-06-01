from django.urls import path, include
from rest_framework.routers import DefaultRouter

from keywords.apis import RelatedKeywordViewSet, FavoriteViewSet

app_name = 'keywords'
favorite_list = FavoriteViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
post_detail = FavoriteViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})
router = DefaultRouter()
router.register('', RelatedKeywordViewSet)


urlpatterns = [
    path('favorite/', favorite_list, name="user-favorite-list"),
    path('favorite/<int:pk>/', post_detail, name="user-favorite-detail"),
    path('', include(router.urls)),


]
