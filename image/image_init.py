import openai
import config
openai.api_key = config.API_KEY;
import base64
import requests
import base64
from PIL import Image
class ImageModel:
    model = None

    def __int__(self, model=None):
        self.model = model
    @classmethod
    def createImage(cls, text,size):
        response = openai.Image.create(prompt=text, n=1, size=size);
        image_url = response["data"][0]["url"];
        return image_url;
