import subprocess
import platform
import os
import paramiko

def supportCmd():
    if platform.system().lower() == 'windows':
        return True
    elif platform.system().lower() == 'linux':
        return True
    else:
        print("unknow OS")
        return False

def put(ip:str, port:int, user:str, password:str, orgPath:str, targetStorage:str, targetPath:str) -> bool:
    if supportCmd():
        """
        cmd = "sshpass -p '" + password + "' scp -o StrictHostKeyChecking=no -P " + port + " " + orgPath + " " + user + "@" + ip + ":/root/" + targetStorage+ "/" + targetFile
        subprocess.run(cmd, shell=True)
        """
        local_path = orgPath
        server_path = os.path.join("/root/" + targetStorage+ "/", targetPath)
        trans = None
        ftp = None
        try:
            trans = paramiko.Transport((ip, port))
            trans.connect(username=user, password=password)
            ftp = paramiko.SFTPClient.from_transport(trans)
            ftp.put(local_path, server_path)
        finally:
            if ftp is not None:
                ftp.close()
            if trans is not None:
                trans.close()

def get(ip:str, port:int, user:str, password:str, remoteStorage:str, remotePath:str, localPath:str) -> bool:
    if supportCmd():

        local_path = localPath
        server_path = os.path.join("/root/" + remoteStorage+ "/", remotePath)
        trans = None
        ftp = None
        try:
            trans = paramiko.Transport((ip, port))
            trans.connect(username=user, password=password)
            ftp = paramiko.SFTPClient.from_transport(trans)
            ftp.get(server_path, local_path)
        finally:
            if ftp is not None:
                ftp.close()
            if trans is not None:
                trans.close()

def ls(ip:str, port:int, user:str, password:str, targetStorage:str, path:str):
    if supportCmd():
        client = None
        path = os.path.join("/root/" + targetStorage+ "/" , path)
        try:
            client = paramiko.SSHClient()
            # automatically add keys without requiring human intervention
            client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
            client.connect(ip, port=port, username=user, password=password)
            ftp = client.open_sftp()
            files = ftp.listdir(path)
        finally:
            if client is not None:
                client.close()
        return files
        

def delete(ip:str, port:int, user:str, password:str, targetStorage:str, targetFile:str):
    if supportCmd():
        """
        cmd = "sshpass -p '" + password + "' ssh -o StrictHostKeyChecking=no -p " + str(port) + " " + user + "@" + ip + " -tt rm -rf /root/" + targetStorage + "/" + targetFile
        subprocess.run(cmd, shell=True)
        """
        if targetFile:
            cmdStr = "rm -rf /root/" + targetStorage + "/" + targetFile
            cmd(ip, port, user, password, cmdStr)            
        else:
            print("targetFile should not be empty or None")

def tar(ip:str, port:int, user:str, password:str, targetStorage:str, targetPath:str, tarFile:str):
    if supportCmd():
        if targetPath and targetStorage and tarFile:
            cmdStr = "cd /root/" + targetStorage + " && " + "tar cvf " + tarFile + " " + targetPath
            cmd(ip, port, user, password, cmdStr)            
        else:
            print("targetFile should not be empty or None")

def untar(ip:str, port:int, user:str, password:str, targetStorage:str, tarFile:str, targetPath:str = None):
    if supportCmd():
        if targetStorage and tarFile:
            targetPath = targetStorage + "/" + targetPath
            tarPath = targetStorage + "/" + tarFile
            if targetPath:
                cmdStr = "mkdir -p "+ targetPath + " && " + "tar xvf " + tarPath + " -C " + targetPath
            else:
                cmdStr = "tar xvf " + tarPath
            cmd(ip, port, user, password, cmdStr)             
        else:
            print("targetFile should not be empty or None")

def cmd(ip:str, port:int, user:str, password:str, cmdStr:str):
    if supportCmd():
        """
        cmd = "sshpass -p '" + password + "' ssh -o StrictHostKeyChecking=no -p " + str(port) + " " + user + "@" + ip + " -tt rm -rf /root/" + targetStorage + "/" + targetFile
        subprocess.run(cmd, shell=True)
        """
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port, user, password)
            std_in, std_out, std_err = client.exec_command(cmdStr)
            out = std_out.read().decode('UTF-8')
            err = std_err.read().decode('UTF-8')
            if out:
                print("out:" + out)
            if err:
                print("err:" + err)
        except Exception as e:
            print("error:" + str(e))
        finally:
            if client is not None:
                client.close() 
