from utils.baseModel import BaseModel;
from peewee import CharField;

class User(BaseModel):
    user_name = CharField();
    phone = CharField();
    password = CharField();

    class Meta:
        table_name = "users";