from flask import Blueprint, jsonify, request
router_blueprint = Blueprint('router', __name__)
from app.controllers.login import LoginController;
from app.controllers.chat import CahtController;
from app.controllers.image import ImageController;
from utils.jwtToken import authenticate;
login_controller = LoginController();
chat_controller = CahtController();
image_controller = ImageController();
@router_blueprint.route('/', methods=['GET', 'POST'])
def test():
    return"测试"

# 注册
@router_blueprint.route('/regist',methods=['POST'])
def regist():
    data = request.get_json();
    return login_controller.register(data);

# 登录
@router_blueprint.route('/login',methods=['POST'])
def login():
    data = request.get_json();
    return login_controller.login(data);


# -------------------------------------- 聊天 -----------------------------------------

# 创建对话
@router_blueprint.route('/chat/create',methods=['POST'])
@authenticate
def createChat():
    data = request.get_json();
    userId = request.user["userId"];
    return chat_controller.createDialogue(data,userId);

# 对话
@router_blueprint.route('/chat/chat',methods=['POST'])
@authenticate
def chat():
    data = request.get_json();
    userId = request.user["userId"];
    return chat_controller.chat(data, userId);

# 删除对话
@router_blueprint.route('/chat/del',methods=['POST'])
@authenticate
def delChat():
    data = request.get_json();
    userId = request.user["userId"];
    return chat_controller.delChat(data["chatId"],userId);

@router_blueprint.route('/chat/chatList',methods=['Get'])
@authenticate
def chatList():
    pageNum = request.args.get("pageNum", default=1, type=int)
    perPage = request.args.get('perPage', default=20, type=int)
    userId = request.user["userId"];
    return chat_controller.getChatList(userId,pageNum,perPage);

# 获取对话详情
@router_blueprint.route('/chat/getMessage',methods=['Get'])
@authenticate
def message():
    chatId = request.args.get("chatId")
    userId = request.user["userId"];
    return chat_controller.getChatMessage(userId,chatId);

# ---------------------------------------------  图片处理 ------------------------------------------

# 创建图片
@router_blueprint.route('/image/create',methods=['POST'])
@authenticate
def createImage():
    data = request.get_json();
    return image_controller.createImage(data);