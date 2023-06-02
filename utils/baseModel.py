from config import DATA_CONFIG;
from flask_peewee.db import *;
from utils.times import getNowText;
database = MySQLDatabase(DATA_CONFIG["database"], user=DATA_CONFIG["user_name"], password=DATA_CONFIG["password"], host=DATA_CONFIG["host"], port=DATA_CONFIG["port"]);

class DoesNotExist(Exception):
    pass
class BaseModel(Model):
    id = AutoField(unique=True,primary_key=True);
    is_del = BooleanField(default=False);
    create_time = DateTimeField();
    update_time = DateTimeField();

    @classmethod
    def creater(cls,insert):
        now = getNowText();
        if "create_time" not in insert:
            insert["create_time"] = now;
        if "update_time" not in insert:
            insert["update_time"] = now;
        cls.create(**insert);

    @classmethod
    def createMany(cls,data):
        now = getNowText();
        for value in data:
            if "create_time" not in value:
                value["create_time"] = now;
            if "update_time" not in value:
                value["update_time"] = now;

        cls.insert_many(data).execute();

    @classmethod
    def findOne(cls,where,fields=[]):
        if "is_del" not in where:
            where["is_del"] = False;

        query = cls.select();
        if len(fields) != 0:
            query = cls.select(**fields);
        try:
            query = query.where(*(getattr(cls, field) == value for field, value in where.items()));
            return query.get();
        except cls.DoesNotExist:
            return None;

    @classmethod
    def list(cls,pageNum,perPage,where,fields=[]):
        if "is_del" not in where:
            where["is_del"] = False;

        query = cls.select().paginate(pageNum,perPage);
        cls.handleSql(query, where);
        query = query.where(*(getattr(cls, field) == value for field, value in where.items()));
        return list(query);

    @classmethod
    def findAll(cls,where,fields=[]):
        if "is_del" not in where:
            where["is_del"] = False;

        query = cls.select();
        if len(fields) != 0:
            query = cls.select(**fields);
        query = cls.handleSql(query,where);
        query = query.where(*(getattr(cls, field) == value for field, value in where.items()));
        return list(query);
    @classmethod
    def updateOne(cls,update,where):
        now = getNowText();
        if "is_del" not in where:
            where["is_del"] = False;
        if "update_time" not in update:
            update["update_time"] = now;
            
        query = cls.update(**update).where(*(getattr(cls, field) == value for field, value in where.items()))
        query.execute();


    @classmethod
    def handleSql(cls,sql,where):
        if "NOT_IN" in where:
            print("1111111111111111111111111111111111111");
            sql = sql.where(where["NOT_IN"][0].not_in(where["NOT_IN"][1]));
            del where["NOT_IN"];

        return sql;

    class Meta:
        database = database;

