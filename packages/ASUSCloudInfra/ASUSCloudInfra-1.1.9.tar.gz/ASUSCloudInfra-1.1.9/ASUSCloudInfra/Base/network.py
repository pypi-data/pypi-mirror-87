from enum import Enum
"""
containerPort: 4242
nodePort: 30929
protocol: "TCP"
"""

class Protocol():
    TCP = "TCP"
    UTP = "UDP"

class Network():
    def __init__(self, containerPort:int, protocol:str, publish:bool=False, nodePort:int=None):
        self._containerPort = containerPort
        if nodePort:
            if nodePort < 30000 or nodePort > 32767:
                raise Exception("nodePort range should be 30000 ~ 32767")
        self._nodePort = nodePort
        self._publish = publish
        self._protocol:Protocol = protocol
    
    def getContainerPort(self) -> int:
        return self._containerPort
    
    def getNodePort(self) -> int:
        return self._nodePort

    def getProtocol(self) -> str:
        return str(self._protocol)

    def isPublish(self) -> bool:
        return self._publish
    
    def getRawData(self):
        data = {}
        if self.isPublish():
            nodePort = self.getNodePort()
            if nodePort:
                data = {
                    'containerPort': self.getContainerPort(),
                    'protocol': self.getProtocol(),
                    'nodePort': nodePort
                }
            else:
                data = {
                    'containerPort': self.getContainerPort(),
                    'protocol': self.getProtocol(),
                }
        else:
            data = {
                'containerPort': self.getContainerPort(),
                'protocol': self.getProtocol(),
            }
        return data
