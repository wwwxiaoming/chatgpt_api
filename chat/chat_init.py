import openai
import config
import uuid
import utils.times as times;
openai.api_key = config.API_KEY;
class ChatModel:
    messages = []; # 全部的聊天消息
    __model = None
    sessionId = None;
    messagesData = []; # 消息数据，里面包括了创建时间
    newMessage = []; #新消息

    def __init__(self, roleText):
        self.model = "gpt-3.5-turbo"
        # if roleText != "":
        #     self.messages.append({"role": "system", "content": roleText})
        unique_id = uuid.uuid4()
        self.sessionId = str(unique_id);

    def handChat(self,sessionId,message = []):
        self.sessionId = sessionId;
        for value in message:
            self.messages.append({"role": value.role, "content": value.message})
            self.messagesData.append({"role": value.role, "content": value.message,"create_time":value.create_time});

    def chat(self, chatText):
        nowTime = times.getNowTime();
        self.messages.append({"role": "user", "content": chatText})
        self.newMessage.append({"role": "user", "content": chatText,"create_time": nowTime})
        self.messagesData.append({"role": "user", "content": chatText, "create_time": nowTime})
        completion = openai.ChatCompletion.create(
            api_key=config.API_KEY,
            model=self.model,
            messages=self.messages,
            max_tokens=2048,
            stop=None,

        )
        nowTimeRes = times.getNowTime();
        answer: str = completion.choices[0].message["content"]
        self.messages.append({"role": "assistant", "content": answer})
        self.newMessage.append({"role": "assistant", "content": answer, "create_time": nowTimeRes})
        self.messagesData.append({"role": "assistant", "content": answer, "create_time": nowTimeRes})
        return answer

    def chat2(self,chatText):
        # self.__messages.append({"role": "user", "content": f"New chat started, ID: {chat_id}"})
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=chatText,
            max_tokens=50,
            temperature=0.7,
            n=1,
            stop=None,
            context=self.sessionId,
        )
        reply = response.choices[0].text.strip()
        return reply
