from typing import List
from .config import IMAGE_ACTION_PREFIX
from .api_token import APIToken

class Tag():
    def __init__(self, dockerImage, rawdata):
        self._dockerImage = dockerImage
        self._rawdata = rawdata

    def getId(self)->str:
        return str(self._rawdata['id'])

    def getName(self)->str:
        return self._rawdata['tag']

    def getStatus(self)->str:
        return self._rawdata['status']

    def getImagePath(self):
        return self._dockerImage.getImagePath()

    def getImagePathWithTag(self)->str:
        return self._dockerImage.getImagePath() + ":" + self.getName()
    

class DockerImage():
    def __init__(self, apiToken:APIToken, rawdata):
        self._apiToken = apiToken
        self._actionPrefix = IMAGE_ACTION_PREFIX + apiToken.getProjectId() + "/"
        self._rawdata = None
        self._tags = []
        self.setRaw(rawdata)
        

    def getId(self)-> str:
        return self._rawdata['id']
    
    def getName(self)-> str:
        return self._rawdata['name']
    
    def getProject(self)-> str:
        return self._rawdata['project_name']

    def getTags(self)-> List[Tag]:
        return self._tags

    def getTag(self, tagName)-> Tag:
        findTag = None
        for tag in self._tags:
            if tagName == tag.getName():
                findTag = tag
                break
        return findTag

    def getImagePath(self)-> str:
        return self._rawdata['path']

    def getRaw(self):
        return self._rawdata
    
    def setRaw(self, rawdata):
        self._rawdata = rawdata
        tagDataList = rawdata['tags']
        tags = []
        if tagDataList is not None:
            for tagData in tagDataList:
                tag = Tag(self, tagData)
                tags.append(tag)
        self._tags = tags

    def refresh(self):
        action = self._actionPrefix + "image/" + self.getId()
        resp = self._apiToken.get(action)
        if "errorCode" in resp and resp['errorCode'] != None:
            return False
        self.setRaw(resp['data'])
        return True

    def createImageTag(self, tagName)->Tag:
        action = self._actionPrefix + "image/" + self.getId() + "/tag"

        body = { 
            'image': {'tag': tagName}
        }
        resp = self._apiToken.post(action, body)
 
        if "errorCode" in resp and resp['errorCode'] != None:
            return None
        tag = Tag(self, resp['data'])
        self.refresh()
        return tag
    
    def deleteImageTag(self, tagName):
        find = None
        for tag in self.getTags():
            if tag.getName() == tagName:
                find = tag
        if find is not None:
            action = self._actionPrefix + "image/" + self.getId() + "/tag/" + find.getId()
            self._apiToken.delete(action)
            self.refresh()
            return True
        else:
            print("deleteImageTag failed. Image tag:" +  tagName + " not found")
        return False

