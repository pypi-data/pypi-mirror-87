from typing import List
from .image_repository import ImageRepository
from .container import Container
from .api_token import APIToken
from .storage_service import getStorageListFromCache
from .enviroment import Enviroment
from .network import Network
from .mount_volume import MountVolume 
from .flavor import Flavor

def getNetwork(data, publish) -> Network:
    containerPort = data['containerPort']
    protocol = data['protocol']
    nodePort = None
    if 'nodePort' in data:
        nodePort = data['nodePort']
    network =  Network(containerPort, protocol, publish, nodePort)
    return network

def getMountVolume(mountData) -> MountVolume:
    #name = mountData['name']
    mountPath = mountData['mountPath']
    pvcName = mountData['pvcName']
    subPath = mountData['subPath']
    storageList = getStorageListFromCache()
    foundStorage = None
    for storage in storageList:
        if pvcName == storage.getPVCName():
            foundStorage = storage
            break
    mountVolume = MountVolume(foundStorage, mountPath, subPath)
    return mountVolume

def getContainer(apiToken:APIToken, containerData) -> Container:
    id = str(containerData['id'])
    name = containerData['name']
    description = containerData['description']
    imagePath = containerData['imageName']
    
    mountVolumes = []
    volumes = containerData['volumes']
    for volume in volumes:
        mountVolume = getMountVolume(volume)
        mountVolumes.append(mountVolume)

    ports = containerData['ports']['nodePort']
    networkList = []
    for port in ports:
        network = getNetwork(port, True)
        networkList.append(network)

    ports = containerData['ports']['clusterIP']
    for port in ports:
        network = getNetwork(port, False)
        networkList.append(network)

    envData = containerData['env']
    enviroment = Enviroment(envData)

    flavorData = containerData['flavor']
    flavor = None
    if flavorData:
        flavor = Flavor(flavorData['id'], flavorData['name'], flavorData)

    command = containerData['command']
    container = Container(name, description, imagePath, flavor, enviroment, mountVolumes, networkList, command)
    container.setId(id)
    container.setAPIToken(apiToken)
    return container

class ContainerService():
    def __init__(self, apiToken:APIToken):
        self._apiToken = apiToken
        self._actionPrefix = "/api/v1/containers/projects/" + apiToken.getProjectId() + "/"
        self._imageRepository = ImageRepository(apiToken)

    def getContainerList(self, imageName=None, project=None):
        getStorageListFromCache(self._apiToken)
        action = self._actionPrefix
        body = self._apiToken.get(action)
        containerList = []
        image = None
        if imageName is not None:
            image = self._imageRepository.getImage(imageName, project)
        #print(image['path'], flush=True)
        for containerData in body:
            container = getContainer(self._apiToken, containerData)
            if image is None:
                containerList.append(container)
            else:
                imageName = container.getImageName()
                if imageName == image.getImagePath():
                    containerList.append(container)
        return containerList
    
    def getContainer(self, containerName):
        containerList = self.getContainerList()
        find = None
        for container in containerList:
            if container.getName() == containerName:
                find = container
                break
        return find
    
    def deleteContainer(self, containerName):
        container = self.getContainer(containerName)
        if container:
            action = self._actionPrefix + container.getId()
            self._apiToken.delete(action)
    
    def updateContainer(self, container:Container):
        action = self._actionPrefix + container.getId()
        resp = self._apiToken.patch(action, container.getUpdate())
        if "errorCode" in resp and resp['errorCode'] != None:
            return None
        container = getContainer(self._apiToken, resp)
        return container

    def createContainer(self, name:str, imagePath:str, flavor:Flavor, enviroment:Enviroment=None, mountList:List[MountVolume]=None, networkList:List[Network]=None, command:str=None):
        action = self._actionPrefix
        #env: [{name: "test", value: "123"}]
        envData = []
        if enviroment:
            envData = enviroment.getRawData()

        volumes = []
        if mountList:
            for mountVolume in mountList:
                volumeData = mountVolume.getRawData()
                volumes.append(volumeData)

        nodePorts = []
        clusterIPs = []
        if networkList:
            for network in networkList:
                if network.isPublish():
                    networkData = network.getRawData()
                    nodePorts.append(networkData)
                else:
                    networkData = network.getRawData()
                    clusterIPs.append(networkData)
        commandData = []
        if command and len(command) > 0:
            commandData = [
                '/bin/sh',
                '-c',
                command
            ]
        body = {
            'name' : name,
            'imageName': imagePath,
            'flavorId': flavor.getId(),
            'env':envData,
            'type': "normal",
            'replica': 1,
            'settings':{},
            'volumes':volumes,
            'ports':{
                'nodePort':nodePorts,
                'clusterIP':clusterIPs
            },
            'command': commandData
        }
        resp = self._apiToken.post(action, body)
        if "errorCode" in resp and resp['errorCode'] != None:
            return None
        container = getContainer(self._apiToken, resp)
        return container
    
    def getContainerHardwareSetting(self) -> List[Flavor]:
        action = "/api/v2/flavors/?type=container"
        flavorDataList = self._apiToken.get(action)
        flavorList = []
        for flavorData in flavorDataList:
            flavorId = flavorData['id']
            name = flavorData['name']
            flavor = Flavor(flavorId, name, flavorData['resource'])
            flavorList.append(flavor)
        return flavorList
        





