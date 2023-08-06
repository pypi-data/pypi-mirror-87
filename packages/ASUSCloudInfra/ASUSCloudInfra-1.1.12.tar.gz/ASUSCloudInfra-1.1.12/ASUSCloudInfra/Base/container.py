
from typing import List
from .network import Network
from .mount_volume import MountVolume 
from .enviroment import Enviroment
from .flavor import Flavor
from .docker_image import DockerImage, Tag
from .storage_service import getStorageListFromCache
from .api_token import APIToken
"""
command: []
createdTime: "2020-08-31T07:14:21.431Z"
description: ""
displayName: "orthancserver"
env: []
extra: null
finishedTime: null
flavor: {id: 2, name: "[02] No GPU", cpu: 10000, memory: 10240, gpu: 0, gpuType: null, network: null,…}
flavorId: 2
id: 71
imageField: {}
imageName: "10.78.26.20:31352/843b5dcb-8d29-441b-b53b-2fce8833d439-pub/qfcnmmee8x9ssl8yfbggya:latest"
labels: null
modifiedTime: "2020-10-16T11:27:18.188Z"
modifier: {id: "c0386085-363c-40a0-9720-199b15b278aa", name: "scott_su@asus.com", email: "scott_su@asus.com",…}
modifierId: "c0386085-363c-40a0-9720-199b15b278aa"
name: "orthancserver"
ports: {nodePort: [{containerPort: 4242, protocol: "TCP", nodePort: 30929},…], clusterIP: []}
projectId: "843b5dcb-8d29-441b-b53b-2fce8833d439"
replica: 1
scalingContentCpu: null
scalingContentMax: null
scalingContentMin: null
scalingContentReplicas: null
scalingType: null
settings: {}
status: "Ready"
type: "normal"
user: {id: "7e2d3d4c-7d23-4a55-85d1-79d35a064103", name: "kevin_chiou@asus.com",…}
userId: "7e2d3d4c-7d23-4a55-85d1-79d35a064103"
volumes: [{pvcName: "90b42ef6-5e8f-4b5e-9597-1251b2838ed7", mountPath: "/etc/orthanc/orthanc.json",…},…]

mountPath: "/mpidata"
name: "kevinmpi"
pvcName: "d9e3a61f-a559-44f2-bb8c-3b0546469d24"
subPath: ""

containerPort: 4242
nodePort: 30929
protocol: "TCP"
"""

class Container():
    """
    def __init__(self, data):
        self._data = None
        self._command = []
        self._mountList = []
        self._networkList = []
        self._env = Enviroment()
        self._flavor = None
        self.setRawData(data)
        self._update = {}
"""
    def __init__(self, name:str, description:str, imagePath:str, hardwareSetting:Flavor, env:Enviroment, mountList:List[MountVolume], networkList:List[Network], command:str):
        self._id = None
        self._name = name
        self._imagePath = imagePath
        if not description:
            description = ""
        self._description = description
        
        self._mountList = mountList
        self._networkList = networkList
        self._env = env
        self._flavor = hardwareSetting
        self._command = [
            "/bin/sh",
            "-c",
            command
        ]
        self._apiToken = None
        self._update = {}

    def setId(self, id:str):
        self._id = id

    def setAPIToken(self, apiToken:APIToken):
        self._apiToken = apiToken

    def getId(self) -> str:
        return self._id

    def getDescription(self) -> str:
        return str(self._description)

    def getName(self) -> str:
        return self._name

    def getImagePath(self) -> str:
        return self._imagePath

    def getImageName(self) -> str:
        lastIndex = self._imagePath.rfind(':')
        return self._imagePath[:lastIndex]

    def getImageTag(self) -> str:
        lastIndex = self._imagePath.rfind(':') + 1
        return self._imagePath[lastIndex:]

    def getMountVolumeList(self) -> List[MountVolume]:
        return self._mountList
    
    def getNetworkList(self) -> List[Network]:
        return self._networkList
    
    def getEnviroment(self) -> Enviroment:
        return self._env

    def getHardwareSetting(self) -> Flavor:
        return self._flavor
        
    def getCommand(self) -> str:
        cmdStr = None
        if self._command:
            defaultCommand = False
            if len(self._command) == 3:
                if self._command[0] == '/bin/sh' and self._command[1] == '-c':
                    defaultCommand = True

            if defaultCommand:
                cmdStr = self._command[2]
            else:
                isFirst = True
                for cmd in self._command:
                    if not isFirst:
                        cmdStr = cmdStr + " "
                    else:
                        isFirst = False
                    cmdStr = cmdStr + cmd
        return cmdStr
    
    def getCommandArray(self) -> List[str]:
        return self._command

    def setCommand(self, command:str):
        if command and len(command) > 0: 
            self._update['command'] = [
                "/bin/sh",
                "-c",
                command
            ]
        else:
            self._update['command'] = []
        return self

    def setEnv(self, env:Enviroment):
        envData = []
        if env:
            envData = env.getRawData() 
        else:
            print("set env but env is empty")
        self._update['env'] = envData
        return self

    def setImage(self, imageTag:Tag):
        if imageTag:
            self._update['imageName'] = imageTag.getImagePathWithTag()
        else:
            print("set Image tag but tag not found")
        return self

    def setNetworkList(self, networks:List[Network]):
        clusterIPs = []
        nodePorts = []
        portArray = []
        for network in networks:
            publish = network.isPublish()
            containerPort = network.getContainerPort()
            if containerPort in portArray:
                raise Exception("container same containerPort:" + str(containerPort))
            else:
                portArray.append(containerPort)
                if publish:
                    nodePort = {
                        "containerPort": containerPort,
                        "protocol": network.getProtocol()
                    }
                    nodePortData = network.getNodePort()
                    if nodePortData:
                        nodePort["nodePort"] = nodePortData
                        print("publish port", flush=True)
                    nodePorts.append(nodePort)
                else:
                    clusterIP = {
                        "containerPort": containerPort,
                        "protocol": network.getProtocol()
                    }
                    print("clusterIP port", flush=True)
                    print("clusterIP containerPort:" + str(clusterIP['containerPort']), flush=True)
                    print("clusterIP protocol:" + str(clusterIP['protocol']), flush=True)
                    clusterIPs.append(clusterIP)
        self._update['ports'] = {
            "clusterIP": clusterIPs,
            "nodePort": nodePorts
        }
        return self

    def setMountVolumeList(self, mountVolumes:List[MountVolume]):
        mountVolumeDatas =[]
        for mountVolume in mountVolumes:
            mountVolumeData = {
                "name":mountVolume.getName(),
                "mountPath":mountVolume.getMountPath(),
                "pvcName":mountVolume.getPVCName(),
                "subPath":mountVolume.getSubPath()
            }
            mountVolumeDatas.append(mountVolumeData)
        self._update['volumes'] = mountVolumeDatas
        return self

    def setDescription(self, desciption:str):
        if not desciption:
            desciption = ""
        self._update['description'] = desciption
        return self
        
    def getUpdate(self):
        return self._update

    def stop(self):
        action = "/api/v1/containers/projects/" + self._apiToken.getProjectId() + "/" + self.getId()+ "/stop"
        self._apiToken.patch(action, None)
    
    def start(self):
        action = "/api/v1/containers/projects/" + self._apiToken.getProjectId() + "/" + self.getId()+ "/restart"
        self._apiToken.patch(action, None)


