import json
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.keyword_api_funtions import required_keyword_function, related_keyword_function, \
    attractive_keyword_function, keyword_analysis_data_collect, get_shopping_list


class RelatedKeywordAPIView(APIView):

    def get(self, request, format=None):
        request_keyword_list = ['금반지', '14K반지', '18K반지', '우정링', '커플링']

        # 여기서 키워드 별로 비동기 처리하고
        # 각각 lanmda 사용해보기

        shopping_keyword_list, list_exists = get_shopping_list(keyword=request_keyword_list[0])
        required_keyword_list = required_keyword_function(shopping_keyword_list)
        related_check_must_key_df, keyword_collect_df = related_keyword_function(shopping_keyword_list,
                                                                                 required_keyword_list)
        attractive_concat_df = attractive_keyword_function(related_check_must_key_df, keyword_collect_df)
        # result_df = keyword_analysis_data_collect(attractive_concat_df, list_exists, request_keyword_list)
        #
        data = json.loads(attractive_concat_df.to_json(orient='records'))
        return Response(data)
