from rest_framework import serializers

from members.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


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
            # "password",
            "company",
            "advertisement_url",
            "naver_api_key",
        )

