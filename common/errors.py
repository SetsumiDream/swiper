SMS_ERROR = 1000
VCODE_ERROR = 1001
LOGIN_REQUIRED = 1002
PROFILE_ERROR = 1003
EXCEED_MAXIMUM_REWIND = 1004
NO_RECORD = 1005


class LogicErr(Exception):
    code = None
    data = None

# 定义一个声称异常类的工厂方法。
def gen_logic_err(name, code, data):
    return type(name, (LogicErr,), {'code': code, 'data': data})


SmsError = gen_logic_err('SmsError', code=1000, data='短信发送失败')
VcodeError = gen_logic_err('VcodeError', code=1001, data='短信验证码不正确')
LoginRequired = gen_logic_err('LoginRequired', code=1002, data='请登录')
ProfileError = gen_logic_err('ProfileError', code=1003, data='资料不合法')
ExceedMaximumRewind = gen_logic_err('ExceedMaximumRewind', code=1004, data='超过反悔次数')
NoRecord = gen_logic_err('NoRecord', code=1005, data='资料不合法')

PermissionDenied = gen_logic_err('PermissionDenied', code=1006, data='权限不足')





# type('SmsError', (LogicErr,), {'code': 1000, 'data': '短信发送失败'})
#
# class SmsError(LogicErr):