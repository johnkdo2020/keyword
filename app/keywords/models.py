from django.db import models

from members.models import User


class Keyword(models.Model):
    name = models.CharField('키워드', max_length=50, )
    favorite_members = models.ManyToManyField(
        User, through='Favorite', related_name='favorite_keyword', help_text='즐겨찾기'
    )
    created_at = models.DateTimeField(
        'Date joined',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Date updated',
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "created_at"],
                name="unique_keyword"
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites')
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='favorites', )
    is_active = models.BooleanField('활성화', default=False)
    created_at = models.DateTimeField(
        'Date joined',
        unique=True,
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Date updated',
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "keyword"],
                name="unique_favorite"
            )
        ]


class RelatedKeyword(models.Model):
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='related_keywords')
    monthly_qc_cnt = models.IntegerField('검색량_전체', default=0)
    monthly_pc_qc_cnt = models.IntegerField('검색량_pc', default=0)
    monthly_mobile_qc_cnt = models.IntegerField('검색량_모바일', default=0)
    monthly_ave_clk_cnt = models.FloatField('클릭수_전체', default=0)
    monthly_ave_pc_clk_cnt = models.FloatField('클릭수_pc', default=0)
    monthly_avg_mobile_clk_cnt = models.FloatField('클릭수_모바일', default=0)
    monthly_ave_ctr = models.FloatField('클릭률_전체', default=0)
    monthly_ave_pc_ctr = models.FloatField('클릭률_PC', default=0)
    monthly_ave_mobile_ctr = models.FloatField('클릭률_모바일', default=0)
    pl_avg_depth = models.IntegerField('월평균노출_광고수', default=0)
    comp_idx = models.CharField('경쟁강도', max_length=15, default='')
    created_at = models.DateTimeField(
        'Date joined',
        unique=True,
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Date updated',
        auto_now=True
    )
