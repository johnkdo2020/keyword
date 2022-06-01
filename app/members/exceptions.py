from rest_framework import status
from rest_framework.exceptions import APIException


class UsernameDuplicateFailException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '존재하는 아이디입니다.'
    default_code = 'DuplicatedUsername'


# 아이디 비밀번호 유효하지 않음
class LoginFailException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '로그인 실패 - email과 password를 확인해주세요.'
    default_code = 'LoginFail'


# 회원가입 유저에게 이메일 보내기 실패(아이디는 만들어짐 문제 확인하기)
class EmailSendFailException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '이메일 보내기 실패 - 서버 설정한 이메일 확인 앱 비밀번호 문제 추측'
    default_code = 'Email Send Fail'


# 유저 pk 와 user token 값 매치 실패
class UserTokenNotMatchFailException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '유저 정보와 유저 토큰값이 불일치 -  Frontend data 관리 결점 혹은 Backend 디비 결점 발생 재구현 루투 확인해서 보완하기'
    default_code = 'User Token Not Match'


# 아이디가 존재하지 않음
# 여러개의 User가 존재할수 있는가 filter로 구현해야하는가?
class UserNotExistsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Username 혹은 Email 존재하지 않음 -  두개 값이 유효하지 않습니다.'
    default_code = 'User Not Exists'


# 임시 비밀번호 생성 실패
class UserTemporaryPasswordCreateFailException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '임시 비밀번호 생성 되 지않음 - Server 쪽에서 코류.'
    default_code = 'Temporary password create Fail'


# 유저 비밀번호 일치하지 않아서 업데이트 실패
class UserPasswordCheckFailException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'User 비밀번호가 일치하지 않습니다.- 비밀번호 재확인 바랍니다.'
    default_code = 'User Password Check Fail'
