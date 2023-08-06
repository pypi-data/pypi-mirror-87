from enum import Enum
from typing import List
from .api_token import APIToken
from .docker_image import DockerImage
from .config import IMAGE_ACTION_PREFIX

class ImageType(Enum):
    ALL = "all"
    PRIVATE = "private"
    PUBLIC = "public"


class ImageRepository():
    def __init__(self, apiToken:APIToken):
        self._apiToken = apiToken
        self._actionPrefix = IMAGE_ACTION_PREFIX + apiToken.getProjectId() + "/"

    def getAllImageList(self)->List[DockerImage]:
        action = self._actionPrefix + "image/service"
        body = self._apiToken.get(action)
        imageDataList = None
        imageDataList = body['data']['public'] + body['data']['private']
        imageList = []
        for imageData in imageDataList:
            image = DockerImage(self._apiToken, imageData)
            imageList.append(image)
        return imageList

    def getImageList(self, imageType:ImageType)->List[DockerImage]:
        action = self._actionPrefix + "image"
        body = self._apiToken.get(action)
        imageDataList = None
        if imageType == ImageType.ALL:
            imageDataList = body['data']['public'] + body['data']['private']
        elif imageType == ImageType.PUBLIC:
            imageDataList = body['data']['public']
        else:
            imageDataList = body['data']['private']
        
        imageList = []
        for imageData in imageDataList:
            image = DockerImage(self._apiToken, imageData)
            imageList.append(image)
        return imageList

    def getImage(self, imageName:str, project:str=None)->DockerImage:
        find = None
        imageList = self.getAllImageList()
        if project is None:
            project = self._apiToken.getProjectName()
        for image in imageList:
            if image.getProject() == project:
                if image.getName() == imageName:
                    find = image
                    break
        return find
    
    
    def createImage(self, imageName:str, description:str="", public:bool=False)->DockerImage:
        action = self._actionPrefix + "image"
        body = { 
            'image': {'name': imageName,
                'description': description,
                'public': public
            }
        }
        resp = self._apiToken.post(action, body)
 
        if "errorCode" in resp and resp['errorCode'] != None:
            return None
        image = DockerImage(self._apiToken, resp['data'])
        return image
    
    def deleteImage(self, imageName:str)->DockerImage:
        image = self.getImage(imageName)
        if image:
            action = self._actionPrefix + "image/" + image.getId()
            resp = self._apiToken.delete(action)


