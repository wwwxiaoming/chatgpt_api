from utils.baseModel import BaseModel;
from peewee import CharField,IntegerField;

class Chat(BaseModel):
    users_id = IntegerField();
    chat_session_id = CharField();
    title = CharField();
    @classmethod
    def addChat(cls,userId,chat):
        print("插入数据库")
        chatData = cls.findOne({"chat_session_id":chat["chat"].sessionId});
        if chatData != None:
            cls.updateOne({"update_time":chat["updateTime"]});
            return ;
        cls.creater({"users_id":userId,"chat_session_id":chat["chat"].sessionId,"create_time":chat["createTime"],"update_time":chat["updateTime"],"title":chat["title"]})

    # @classmethod
    # def findAll(cls,where,fields=[]):
    #     if "is_del" not in where:
    #         where["is_del"] = False;
    #
    #     query = Chat.select();
    #     # if len(fields) != 0:
    #     #     query = Chat.select(**fields);
    #     # print("2222222222222222222222222222222222222");
    #     # if "NOT_IN" in where:
    #     #     query.where(Chat.chat_session_id.not_in(['7261c809-9679-4a6c-8f93-8230b8bec131']));
    #     #     print(query);
    #     #     del where["NOT_IN"];
    #     notQu = Chat.select().where(Chat.chat_session_id.in_(['7261c809-9679-4a6c-8f93-8230b8bec131']))
    #     query = Chat.select().where(Chat.chat_session_id.not_in(['7261c809-9679-4a6c-8f93-8230b8bec131']));
    #     # query = query.where(*(getattr(Chat, field) == value for field, value in where.items()));
    #     print(query);
    #     return list(query);

    class Meta:
        table_name = "chat";