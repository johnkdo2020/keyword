from rest_framework import status
from rest_framework.exceptions import APIException


# Sign Up
class AlreadyFavoriteKeywordExistsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '이미 즐겨찾기에 추가 되어있습니다.'
    default_code = 'AlreadyFavoriteKeywordExists'

class NotFoundFavoriteKeywordException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '즐겨찾기에 존재하지 않습니다.'
    default_code = 'NotFoundFavoriteInstance'