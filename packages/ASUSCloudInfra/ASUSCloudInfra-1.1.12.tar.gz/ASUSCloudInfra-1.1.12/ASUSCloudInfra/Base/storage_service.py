from enum import Enum
from typing import List
from .api_token import APIToken
from .storage import Storage
from .sftp_client import SFTPClient

class StorageService():
    def __init__(self, apiToken:APIToken):
        self._apiToken = apiToken
        #http://10.78.26.20:31382/api/v1/storage-svc/project/843b5dcb-8d29-441b-b53b-2fce8833d439/storage
        self._actionPrefix = "/api/v1/storage-svc/project/" + apiToken.getProjectId() + "/"

    def getSFTPClient(self) -> SFTPClient:
        #http://10.78.26.20:31382/api/v1/storage-svc/project/843b5dcb-8d29-441b-b53b-2fce8833d439/storageservice
        action = self._actionPrefix + "storageservice"
        body = self._apiToken.get(action)
        if body['errorCode'] is not None:
            print("get storage server fail." + body['error'])
            return None
        sftpClient = SFTPClient(body['data']['url'], body['data']['account'], body['data']['password'])
        return sftpClient

    def getStorageList(self) -> List[Storage]:
        sftpClient = self.getSFTPClient()
        action = self._actionPrefix + "storage"
        body = self._apiToken.get(action)
        if body['errorCode'] is not None:
            print("get storage fail." + body['error'])
            return None
        storageList = []
        storageDataList = body['data']
        for storageData in storageDataList:
            storage = Storage(sftpClient, storageData)
            storageList.append(storage)
        return storageList

    def getStorage(self, name:str) -> Storage:
        storageList = self.getStorageList()
        findStorage = None
        for storage in storageList:
            if storage.getName() == name:
                findStorage = storage
                break
        return findStorage

    def createStorage(self, name:str, description:str="") -> Storage:
        action = self._actionPrefix + "storage"
        sftpClient = self.getSFTPClient()
        body = { 
            'storage': {
                'name': name,
                'description': description
            }
        }
        resp = self._apiToken.post(action, body)
 
        if "errorCode" in resp and resp['errorCode'] != None:
            print("error:" + resp['error'])
            return None
        storage = Storage(sftpClient, resp['data'])
        return storage

    def deleteStorage(self, name:str) -> bool:
        storage = self.getStorage(name)
        if storage:
            action = self._actionPrefix + "storage/" + storage.getId()
            resp = self._apiToken.delete(action)
            if "errorCode" in resp and resp['errorCode'] != None:
                print("error:" + resp['error'])
                return False
            return True
        else:
            print("storage:" + name + " is not found")
            return False

storageList = []
def getStorageListFromCache(api:APIToken=None):
    global storageList
    refresh = False
    if api is not None:
        refresh = True
    if refresh:
        storageService = StorageService(api)
        storageList = storageService.getStorageList()
    return storageList
        




