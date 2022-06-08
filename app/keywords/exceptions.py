from rest_framework import status
from rest_framework.exceptions import APIException


class AlreadyFavoriteKeywordExistsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '이미 즐겨찾기에 추가 되어있습니다.'
    default_code = 'AlreadyFavoriteKeywordExists'


class NotFoundFavoriteKeywordException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '즐겨찾기에 존재하지 않습니다.'
    default_code = 'NotFoundFavoriteInstance'


class RelatedAPIErrorException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '관련 검색어 BAD REQUEST'
    default_code = 'keyword 라는 data 문자열 하나만 보내면 됨'


class RelatedAPINaverAPIProblemException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '관련 검색어 Naver API BAD REQUEST'
    default_code = 'Naver API error 확인'


class RelatedAPIBackendProblemException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = '관련 검색어 Server 문제'
    default_code = '서버 점검해봐야 함'
