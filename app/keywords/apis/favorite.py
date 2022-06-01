from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from keywords.exceptions import AlreadyFavoriteKeywordExistsException, NotFoundFavoriteKeywordException
from keywords.models import Keyword, Favorite
from keywords.serializers import FavoriteSerializer


class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            obj = self.queryset.get(pk=self.kwargs['pk'])
        except:
            raise NotFoundFavoriteKeywordException
        return obj

    def get_queryset(self):
        query_set = self.queryset.filter(user=self.request.user)
        return query_set

    def list(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        user = self.request.user
        favorite_keyword = Favorite.objects.filter(
            keyword__name=self.request.data['name'],
            user=user
        )

        if favorite_keyword.exists():
            raise AlreadyFavoriteKeywordExistsException
        else:
            keyword, _ = Keyword.objects.get_or_create(
                name=self.request.data['name'],
                created_at=timezone.localtime()
            )
        serializer.save(user=user, keyword=keyword)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
