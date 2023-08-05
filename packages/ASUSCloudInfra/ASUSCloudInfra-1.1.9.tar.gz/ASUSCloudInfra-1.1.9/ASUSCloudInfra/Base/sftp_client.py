from ..SFTP import *

class SFTPClient():
    def __init__(self, url, user:str, password:str):
        lastIndex = url.rfind(':')
        firstStr = 'scp://'
        firstIndex = url.find(firstStr) + len(firstStr)
        self._ip = url[firstIndex:lastIndex]
        self._port = int(url[lastIndex + 1:])
        self._user = user
        self._password = password
    
    def getIP(self):
        return self._ip

    def getPort(self):
        return self._port

    def getUser(self):
        return self._user

    def getPassword(self):
        return self._password

    def put(self, orgPath:str, targetStorage:str, targetPath:str) -> bool:
        return put(self._ip, self._port, self._user, self._password, orgPath, targetStorage, targetPath)
    
    def get(self, remoteStorage:str, remotePath:str, localPath:str) -> bool:
        return get(self._ip, self._port, self._user, self._password, remoteStorage, remotePath, localPath)

    def ls(self, targetStorage:str, path:str):
        return ls(self._ip, self._port, self._user, self._password, targetStorage, path)

    def delete(self, targetStorage:str, targetFile:str):
        return delete(self._ip, self._port, self._user, self._password, targetStorage, targetFile)

    def tar(self, targetStorage:str, targetPath:str, tarFile:str):
        return tar(self._ip, self._port, self._user, self._password, targetStorage, targetPath, tarFile)

    def untar(self, targetStorage:str, tarFile:str, targetPath:str = None):
        return untar(self._ip, self._port, self._user, self._password, targetStorage, tarFile, targetPath)

    def cmd(self, cmdStr:str):
        return cmd(self._ip, self._port, self._user, self._password, cmdStr)