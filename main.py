from chat.chat_init import ChatModel
import config
from image.image_init import ImageModel;

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def main():
    chat = ChatModel(config.ROLE_TEXT["Ordinary"])
    print(chat.chat("python中的OpenAI GPT-3.5 API如何通过create方法返回的id进行聊天"))
    # print(chat.chat("数字1的后面是几?"))

    # image = ImageModel();
    # print(image.createImage("雪中的教堂"));


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
