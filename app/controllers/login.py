from flask import request, jsonify;
from app.models.userModel import User;
from passlib.hash import pbkdf2_sha256 as hash_password;
import config;
from utils.phone import encrypt_phone_number;
from utils.jwtToken import generate_token
from utils.response import httpOk200,httpError400
class LoginController:

    # 注册用户
    @staticmethod
    def register(data):
        insterData = {
            "user_name":data["name"],
        }
        insterData["password"] = hash_password.hash(data["password"],salt=config.HASH_KEY.encode('utf-8'));
        insterData["phone"] =encrypt_phone_number(data["phone"]);
        insertId = User.creater(insterData);

        token = generate_token({"userId":insertId});
        return httpOk200({"token":token});

    # 登录
    @staticmethod
    def login(data):
        user = User.findOne({"user_name":data["name"]});
        if user:
            if not hash_password.verify(data["password"],user.password):
                return httpError400("密码不正确");
            else:
                token = generate_token({"userId": user.id});
                return httpOk200({"token":token});
        else:
            return httpError400('用户不存在');
