from utils.baseModel import BaseModel;
from peewee import CharField,IntegerField,TextField;

class ChatMessage(BaseModel):
    users_id = IntegerField();
    chat_session_id = CharField();
    role = CharField();
    message = TextField();

    class Meta:
        table_name = "chat_message";