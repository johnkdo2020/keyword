from django.urls import path

from analysis.apis import RelatedKeywordAPIView

urlpatterns = [
    path('related/', RelatedKeywordAPIView.as_view(), name='related')

]
