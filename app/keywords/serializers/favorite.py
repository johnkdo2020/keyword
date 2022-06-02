from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from keywords.exceptions import AlreadyFavoriteKeywordExistsException
from keywords.models import Favorite, Keyword
from keywords.serializers.keyword import KeywordSerializer
from members.serializers import UserFavoriteSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    user = UserFavoriteSerializer(required=False, read_only=True)
    keyword = KeywordSerializer(required=False, )

    class Meta:
        model = Favorite
        fields = (
            'pk',
            'user',
            'keyword',
            'is_active'
        )


    # def create(self, validated_data):
    #     favorite_keyword_exists = Favorite.objects.filter(
    #         keyword__name=self.initial_data['name'],
    #         user=self.context['request'].user
    #     )
    #     if favorite_keyword_exists:
    #         raise AlreadyFavoriteKeywordExistsException
    #     return attrs

# class FavoriteListSerializer(serializers.ModelSerializer):
#     user = UserFavoriteSerializer(required=False, read_only=True)
#     keyword = KeywordFavoriteSerializer(required=False,)
#
#     class Meta:
#         model = Favorite
#         fields = "__all__"
