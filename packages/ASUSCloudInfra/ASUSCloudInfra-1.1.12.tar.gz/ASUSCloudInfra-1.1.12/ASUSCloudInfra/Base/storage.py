from distutils.util import strtobool
from .sftp_client import SFTPClient
import os
import tarfile
import uuid

def _extract(tar_path, target_path):
    tar = None
    try:
        tar = tarfile.open(tar_path, "r")
        file_names = tar.getnames()
        for file_name in file_names:
            tar.extract(file_name, target_path)
        
    except Exception as e:
        print(str(e))
    finally:
        if tar:
            tar.close()

def _tar_dir(tar_path, target_path):
    tar = None
    try:
        tar = tarfile.open(tar_path, "w")
        oriPath = os.getcwd()
        for root, dirs, files in os.walk(target_path):
            os.chdir(target_path)
            os.chdir('..')
            path = os.getcwd()
            root_ = os.path.relpath(root,start=path)
            for filename in files:
                tar.add(os.path.join(root, filename),arcname=os.path.join(root_,filename))
            for dir in dirs:
	            tar.add(os.path.join(root, dir),arcname=os.path.join(root_,dir)) 
    finally:
        if tar:
            tar.close()
        if oriPath:
            os.chdir(oriPath)
            path = os.getcwd()

"""



createdAt: 1598364795053
creator: null
deletedAt: null
description: "ASUS Cloudinfra System"
editable: false
id: 1
k8s_pvc: "system"
name: "system"
project_id: "843b5dcb-8d29-441b-b53b-2fce8833d439"
removedAt: null
size: "500"
status: "created"
type: "nfs"
updatedAt: null
updator: null

"""

class Storage():
    def __init__(self, sftpClient:SFTPClient, data):
        self._sftpClient = sftpClient
        self._data = data
    
    def getId(self) -> str:
        return str(self._data['id'])
    
    def getName(self) -> str:
        return self._data['name']

    def getDescription(self) -> str:
        return self._data['description']

    def getEditable(self) -> bool:
        return strtobool(self._data['editable'])

    def getPVCName(self) -> str:
        return self._data['k8s_pvc']

    def checkStorageCreated(self):
        return self._sftpClient.checkIfFolderExisted(self.getName())

    def put(self, oriFilePath, targetFilePath:str):
        return self._sftpClient.put(oriFilePath, self.getName(), targetFilePath)
    
    def get(self, remotePath:str, localPath:str) -> bool:
        return self._sftpClient.get(self.getName(), remotePath, localPath)

    def ls(self, path:str = ""):
        return self._sftpClient.ls(self.getName(), path)

    def delete(self, targetFile:str):
        return self._sftpClient.delete(self.getName(), targetFile)

    def tar(self, targetPath:str, tarFile:str):
        return self._sftpClient.tar(self.getName(), targetPath, tarFile)

    def untar(self, tarFile:str, targetPath:str = None):
        return self._sftpClient.untar(self.getName(), tarFile, targetPath)

    def getDir(self, remotePath:str, localPath:str = "") -> bool:
        tarPath = str(uuid.uuid1()) + ".tar"
        try:
            self.tar(remotePath, tarPath)
            self.get(tarPath, tarPath)
        finally:
            self.delete(tarPath)
        
        try:
            _extract(tarPath, localPath)
        finally:
            os.remove(tarPath)

    def putDir(self, localPath:str, remotePath:str ="") -> bool:
        tarPath = str(uuid.uuid1()) + ".tar"
        try:
            _tar_dir(tarPath, localPath)
            self.put(tarPath, tarPath)
        finally:
            os.remove(tarPath)
            
        try:
            self.untar(tarPath, remotePath)
        finally:
            self.delete(tarPath)

        
        

