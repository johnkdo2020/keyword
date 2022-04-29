
def message(domain, pk, token):
    return f"아래 링크를 클릭하면 회원가입 인증이 완료 됩니다. " \
           f"\n\n회원가입 링크 : http://{domain}/api/v1/members/active/{pk}/{token}/" \
           f"\n\n 갑사합니다"


def temporary_password_message(email, password):
    return f"임시 비밀번호가 발행 되었습니다. " \
           f"\n\n회원 ID  : {email} " \
           f"\n\n임시 비밀번호  : {password} " \
           f"\n\n 갑사합니다"