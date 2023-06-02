from flask import Flask
from utils.baseModel import database;
from app.routers import router_blueprint;
from flask_cors import CORS
from utils.schedule import scheduler;
app = Flask(__name__);

# 解决跨域
CORS(app)

app.config.from_object('config');
app.register_blueprint(router_blueprint);

# 定时任务
scheduler.init_app(app)
scheduler.start()

@app.before_request
def before_request():
    database.connect()

@app.after_request
def after_request(response):
    database.close()
    return response;


# 启动服务，开启多线程、debug模式
# 浏览器访问http://127.0.0.1:8088/ai?content="你好"
app.run(
    host=app.config["IP"],
    port=app.config["PORT"],
    threaded=True,
    debug=True
)
