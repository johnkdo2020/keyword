from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractUser)
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):

    def create_user(self, email, username, password, **extra_fields):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not email:
            raise ValueError(_("Users must have an email address"))
        username = self.model.normalize_username(username)
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        user.is_active = False
        user.is_staff = False
        user.is_superuser = False
        user.level = 1

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다.
        """
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields

        )
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.level = 100
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name=_('username'),
        max_length=30,
        unique=True
    )
    company = models.CharField(
        verbose_name=_('company name'),
        max_length=30,
        blank=True,
        null=True)
    advertisement_url = models.CharField(
        verbose_name=_('광고 URL '),
        max_length=255,
        blank=True,
        null=True)
    level = models.IntegerField(
        verbose_name=_('user level'),
        default=0)
    unique_id = models.CharField(
        verbose_name=_('google Id'),
        max_length=50,
        blank=True)
    mobile = PhoneNumberField(
        verbose_name=_('mobile phone number'),
        unique=True,
        null=False,
        blank=False,
        max_length=30, )

    naver_api_key = models.CharField(
        verbose_name=_('naver api Key'),
        max_length=255,
        blank=True,
        null=True,
        unique=True)
    is_active = models.BooleanField(
        verbose_name=_('Is active'),
        default=False
    )
    is_admin = models.BooleanField(
        verbose_name=_('Is admin'),
        default=False
    )
    created_at = models.DateTimeField(
        verbose_name=_('Date joined'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Date updated'),
        auto_now=True
    )
    # 이 필드는 레거시 시스템 호환을 위해 추가할 수도 있다.
    salt = models.CharField(
        verbose_name=_('Salt'),
        max_length=10,
        blank=True
    )
    # favorites = models.ManyToManyField(
    #     Channel, through='Favorite', related_name='users', help_text='즐겨찾기'
    # )
    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'mobile',]

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = '%s 목록' % verbose_name
        ordering = ('-date_joined',)

    def __str__(self):
        return f'{self.email}'
