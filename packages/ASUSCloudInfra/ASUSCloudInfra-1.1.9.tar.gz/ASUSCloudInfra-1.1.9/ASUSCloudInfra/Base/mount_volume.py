from .storage import Storage
class MountVolume():
    def __init__(self, storage:Storage, mountPath:str, subPath:str=""):
        if storage:
            self._name = storage.getName()
            self._PVCName = storage.getPVCName()
        else:
            self._name = "storage not found"
            self._PVCName = None
        self._mountPath = mountPath
        self._subPath = subPath

    def getName(self) -> str:
        return self._name

    def getMountPath(self) -> str:
        return self._mountPath

    def getPVCName(self) -> str:
        return self._PVCName

    def getSubPath(self) -> str:
        return self._subPath

    def getRawData(self):
        data = {
            'name': self.getName(),
            'pvcName': self.getPVCName(),
            'mountPath': self.getMountPath(),
            'subPath': self.getSubPath()
        }
        return data