import jwt
import config
import datetime

from functools import wraps
from flask import Flask, request, jsonify
from utils.response import httpError400,httpError403

def generate_token(payload):
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=1);
    token = jwt.encode(payload, config.SECRET_KEY, algorithm='HS256')
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=['HS256'])
        return {"res":True,"payload":payload}
    except jwt.ExpiredSignatureError:
        # Token 已过期
        return {"res":False,"message":"鉴权过期，请重新登录"}
    except jwt.InvalidTokenError:
        # Token 无效
        return {"res":False,"message":"鉴权无效"}


# 自定义鉴权装饰器
def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 在这里进行鉴权逻辑判断
        # 可以检查请求头、请求参数、会话状态等进行用户验证
        # 如果验证失败，可以返回相应的错误响应，如 401 Unauthorized

        # 示例：检查请求头中是否包含有效的身份令牌
        token = request.headers.get('Authorization')
        if not token:
            return httpError403("未传递token")

        userData = verify_token(token);
        if userData["res"] == False:
            return httpError403(userData["message"]);

        request.user = userData["payload"];

        # 验证通过，继续执行原始的路由函数
        return func(*args, **kwargs)

    return wrapper