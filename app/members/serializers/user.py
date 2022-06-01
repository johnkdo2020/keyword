from rest_framework import serializers

from members.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            "email",
            "password",
            "mobile",
            "company",
            "advertisement_url",
        )

    def save(self, **kwargs):
        self.is_valid(raise_exception=True)
        validated_data = self.validated_data
        password = validated_data['password']
        member = User.objects.create(**validated_data)
        member.set_password(password)
        member.save()
        return member


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "mobile",
            "company",
            "advertisement_url",
            "naver_api_key",
        )

    def update(self, instance, validated_data):
        print('serializer update method')
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.company = validated_data.get('company', instance.company)
        instance.advertisement_url = validated_data.get('advertisement_url', instance.advertisement_url)
        instance.naver_api_key = validated_data.get('naver_api_key', instance.naver_api_key)
        instance.save()
        return instance


class UserFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)
