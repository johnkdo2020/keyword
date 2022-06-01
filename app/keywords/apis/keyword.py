import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import pandas as pd

from keywords.models import Keyword
from keywords.serializers import KeywordSerializer
from utils.keyword_api_funtions import rel_keyword_api
from utils.keyword_proccessing import list_split


class RelatedKeywordViewSet(ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

    def create(self, request, *args, **kwargs):
        related_keyword_df = pd.DataFrame()
        origin_keyword_list_df = pd.DataFrame()

        request_keyword_list = list_split(request.data, 5)

        for split_list in request_keyword_list:
            df = rel_keyword_api(split_list)
            # request keyword data list
            in_request_keyword_list_df = df[df.relKeyword.isin(split_list)]
            origin_keyword_list_df = pd.concat([origin_keyword_list_df, in_request_keyword_list_df], ignore_index=True,
                                               sort=False)

            # 경쟁률 >=15 필터링 && 월평균 pc, m 기준 정렬
            df = df[df.relKeyword.isin(split_list) == False]
            df["monthlyPcQcCnt"] = pd.to_numeric(df["monthlyPcQcCnt"].replace("< 10", "1"))
            df["monthlyMobileQcCnt"] = pd.to_numeric(df["monthlyMobileQcCnt"].replace("< 10", "1"))
            df = df[df['plAvgDepth'] >= 15]
            df = df.sort_values(by=['monthlyPcQcCnt', 'monthlyMobileQcCnt'], ascending=False)
            related_keyword_df = pd.concat([related_keyword_df, df[:10]], ignore_index=True, sort=False)
        result_df = pd.concat([origin_keyword_list_df, related_keyword_df], ignore_index=True, sort=False)
        result_df["monthlyPcQcCnt"] = pd.to_numeric(result_df["monthlyPcQcCnt"].replace("< 10", "1"))
        result_df["monthlyMobileQcCnt"] = pd.to_numeric(result_df["monthlyMobileQcCnt"].replace("< 10", "1"))
        result_df['monthly_qc_cnt'] = result_df[['monthlyPcQcCnt', 'monthlyMobileQcCnt']].sum(axis=1).values
        result_df['monthly_ave_clk_cnt'] = result_df[['monthlyAvePcClkCnt', 'monthlyAveMobileClkCnt']].sum(
            axis=1).values
        result_df['monthly_ave_ctr'] = result_df[['monthlyAvePcCtr', 'monthlyAveMobileCtr']].sum(axis=1).values
        result_df.columns = [
            'keyword', 'monthly_pc_qc_cnt', 'monthly_mobile_qc_cnt', 'monthly_ave_pc_clk_cnt',
            'monthly_avg_mobile_clk_cnt', 'monthly_ave_pc_ctr', 'monthly_ave_mobile_ctr',
            'pl_avg_depth', 'comp_idx', 'monthly_qc_cnt', 'monthly_ave_clk_cnt', 'monthly_ave_ctr'
        ]

        return Response(json.loads(result_df.to_json(orient="table")), status=status.HTTP_200_OK)


