import requests
import jwt
from typing import List
from .api_token import APIToken
from .image_repository import ImageRepository, ImageType
from .container_service import ContainerService
from .docker_image import DockerImage
from .storage_service import StorageService
from .container import Container
from .enviroment import Enviroment
from .network import Network
from .mount_volume import MountVolume 
from .flavor import Flavor

class Project():
    def __init__(self, baseURL, apiToken, port=31382):
        self._apiToken = APIToken(baseURL, apiToken, port)
        self._imageRepository = ImageRepository(self._apiToken)
        self._containerService = ContainerService(self._apiToken)
        self._storageService = StorageService(self._apiToken)

    def getProjectId(self)-> str:
        return self._apiToken.getProjectId()

#image service
    def getAllImageList(self)-> List[DockerImage]:
        return self._imageRepository.getAllImageList()

    def getImageList(self, imageType = ImageType.ALL)-> List[DockerImage]:
        return self._imageRepository.getImageList(imageType)
    
    def getImage(self, imageName, project:str=None)->DockerImage:
        return self._imageRepository.getImage(imageName, project)
    
    def createImage(self, imageName:str, description:str="", public:bool=False)->DockerImage:
        return self._imageRepository.createImage(imageName, description, public)

    def deleteImage(self, imageName:str)->DockerImage:
        return self._imageRepository.deleteImage(imageName)

#container service
    def getContainerList(self, imageName:str=None, project:str=None):
        return self._containerService.getContainerList(imageName)
    
    def getContainer(self, containerName:str) -> Container:
        return self._containerService.getContainer(containerName)
    
    def createContainer(self, name:str, imagePath:str, flavor:Flavor, enviroment:Enviroment=None, mountList:List[MountVolume]=None, networkList:List[Network]=None, command:str=None) -> Container:
        return self._containerService.createContainer(name, imagePath, flavor, enviroment, mountList, networkList, command)

    def updateContainer(self, contaienr:Container) -> Container:
        return self._containerService.updateContainer(contaienr)

    def deleteContainer(self, containerName:str) -> Container:
        return self._containerService.deleteContainer(containerName)

    def getContainerHardwareSetting(self) -> List[Flavor]:
        return self._containerService.getContainerHardwareSetting()

#storage service
    def getStorageList(self):
        return self._storageService.getStorageList()

    def getStorage(self, storageName:str=None):
        return self._storageService.getStorage(storageName)
    
    def createStorage(self, storageName:str=None):
        return self._storageService.createStorage(storageName)

    def deleteStorage(self, storageName:str=None):
        return self._storageService.deleteStorage(storageName)

    def getSFTPClient(self):
        return self._storageService.getSFTPClient()

    

