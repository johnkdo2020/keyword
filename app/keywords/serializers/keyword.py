from rest_framework import serializers

from keywords.models import Keyword, RelatedKeyword


class RelatedKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedKeyword
        fields = "__all__"


class KeywordSerializer(serializers.ModelSerializer):
    related_keywords = RelatedKeywordSerializer(required=False, many=True)

    class Meta:
        model = Keyword
        fields = "__all__"


class KeywordFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        exclude = ("favorite_members",)