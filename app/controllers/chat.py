from app.models.userModel import User;
from utils.response import httpError400,httpOk200;
from chat.chat_init import ChatModel;
from app.models.chatMessageModel import ChatMessage;
import config;
import datetime;
ChatModelMap = {};
from app.models.chatModel import Chat;
import utils.ComKey as ComKey;
import utils.times as times;
import json
class CahtController:
    def createDialogue(self,data,userId):
        now = times.getNowTime();
        user = User.findOne({"id":userId});
        if not user:
            return httpError400("用户不存在");
        startText = ""
        if(config.ROLE_TEXT[data["role"]] == ""):
            startText = data["title"];
        else:
            startText = config.ROLE_TEXT[data["role"]];
        chat = ChatModel(startText);
        if userId not in ChatModelMap:
            ChatModelMap[userId] = {};
        ChatModelMap[userId][chat.sessionId] = {"createTime":now,"updateTime":now,"chat":chat,"title":data["title"]};
        return httpOk200({"chat_session_id":chat.sessionId,"update_time":now.strftime(ComKey.TIME_STRING),"title":data["title"]});

    def chat(self,data,userId):
        now = times.getNowTime();
        if userId not in ChatModelMap:
            return httpError400("用户不存在");
        if data["chatId"] not in ChatModelMap[userId]:
            return httpError400("对话不存在");
        chat = ChatModelMap[userId][data["chatId"]];
        if(chat['title'] == "新建聊天"):
            chat['title'] = data["text"];
        chat["updateTime"] = now;
        message = chat["chat"].chat(data["text"]);
        return httpOk200(message);


    def delChat(self,chatId,userId):
        if userId not in ChatModelMap:
            return httpError400("用户不存在");
        if chatId not in ChatModelMap[userId]:
            return httpError400("对话不存在");
        del ChatModelMap[userId][chatId];

        return httpOk200();

    def getChatList(self,userId,pageNum,perPage):
        notsceneId = [];
        if userId not in ChatModelMap:
            ChatModelMap[userId] = {};

        for sceneId in ChatModelMap[userId]:
            notsceneId.append(sceneId)
        chatList = Chat.findAll({"users_id":userId,"NOT_IN":[Chat.chat_session_id,notsceneId]});
        newList = [];
        for list in chatList:
            newList.append({
                "users_id": list.users_id,
                "chat_session_id": list.chat_session_id,
                "title": list.title,
                "update_time": list.update_time,
            })
        for userId in ChatModelMap:
            for sceneId in ChatModelMap[userId]:
                chatData = ChatModelMap[userId][sceneId];
                newList.append({
                    "users_id":userId,
                    "chat_session_id":sceneId,
                    "title":chatData["title"],
                    "update_time":chatData["updateTime"].strftime(ComKey.TIME_STRING),
                })
        return httpOk200(newList);

    # 获取对话详情
    def getChatMessage(self,userId,sceneId):
        if userId not in ChatModelMap:
            ChatModelMap[userId] = {};
        if sceneId not in ChatModelMap[userId]:
            chatData = Chat.findOne({"users_id":userId,"chat_session_id":sceneId});
            if chatData == None:
                return httpError400("对话不存在");
            chatMessage = ChatMessage.findAll({"users_id":userId,"chat_session_id":sceneId});
            chat = ChatModel('');
            chat.handChat(chatData.chat_session_id,chatMessage);
            ChatModelMap[userId][chat.sessionId] = {"createTime": chatData.create_time, "updateTime": chatData.update_time, "chat": chat,
                                                    "title": chatData.title};
            return httpOk200(chat.messagesData);
        else:
            ChatModelMap[userId][sceneId]["updateTime"] = times.getNowTime();
            return httpOk200(ChatModelMap[userId][sceneId]["chat"].messagesData);

# 倒计时处理久没有响应过的聊天，超过一个小时没有访问过的聊天直接消耗然后存进数据库里面
def SchRemoveChat():
    now = times.getNowTime() - datetime.timedelta(hours=1);
    for userId in ChatModelMap:
        for sceneId in ChatModelMap[userId]:
            chatData = ChatModelMap[userId][sceneId];
            if chatData["updateTime"] <= now:
                Chat.addChat(userId,chatData);
                appData = [];
                for messageValue in chatData["chat"].newMessage:
                    appData.append({"users_id":userId,"chat_session_id":sceneId,"role":messageValue["role"],"message":messageValue["content"],"create_time":messageValue["create_time"],"update_time":messageValue["create_time"]});
                ChatMessage.createMany(appData);
                # 注意：删除字典时，一定要返回新的字典才行
                del ChatModelMap[userId][sceneId];
                return ChatModelMap;




