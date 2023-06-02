# import threading
# class Schedule:
#     schList = [];
# 
#     # 相隔多少秒执行一次
#     def registerTask(self,time,task):
#         print(time);
#         print(task);
#         timer = threading.Timer(time, task)
#         timer.start()
#         self.schList.append(timer);
#         return;
# 
#     # 每周期执行一次，比如每天1点执行一次
#     def registerIntTask(self):
#         return;


from app.controllers.chat import SchRemoveChat;
from flask_apscheduler import APScheduler


scheduler = APScheduler()


# interval example, 间隔执行, 每10分钟执行一次
@scheduler.task('interval', id='do_job_1', seconds=60*10, misfire_grace_time=900)
def SchedulerRemoveChat():
    SchRemoveChat();