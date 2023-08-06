"""
flavor: {id: 2, name: "[02] No GPU", cpu: 10000, memory: 10240, gpu: 0, gpuType: null, network: null,…}
flavorId: 2

createdTime: "2020-08-25T14:43:02.775Z"
finishedTime: null
id: 4
metadata: {}
name: "[04] T4-Network50G"
resource: {cpu: 10000, memory: 40960, gpu: 2, gpuType: "t4", network: "50Gb"}
status: "System"
"""
class Flavor():
    def __init__(self, id, name, data):
        self._id = str(id)
        self._name = name
        self._data = data
    
    def getId(self):
        return self._id
    
    def getName(self):
        return self._name

    def getCPU(self):
        return self._data['cpu'] / 1000 

    def getMemory(self):
        return self._data['memory'] / 1024

    def getGPU(self):
        return self._data['gpu']

    def getGPUType(self):
        return self._data['gpuType']

    def getNetwork(self):
        return self._data['network']