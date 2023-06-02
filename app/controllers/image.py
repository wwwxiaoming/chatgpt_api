from utils.response import httpError400,httpOk200;
from image.image_init import ImageModel;

class ImageController:
    def createImage(self,data):
        url = ImageModel.createImage(data["text"],data["size"]);
        return httpOk200(url);