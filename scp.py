


import os
import sys
import json
import numpy as np


class SCP():

    def __init__(self):
        self.cf_fn = '/home/mph/lib/tool/scp_config.json'
        self.cf = self.read_config(self.cf_fn)
        self.host = self.cf['host']
        self.device_list = self.cf['device_list']
        self.paths = self.cf['paths']


    def read_config(self, cf_fn):
        fr = open(cf_fn, 'r')
        cf = json.load(fr)
        fr.close()
        return cf
    
    def save_config(self, cf, cf_fn):
        fw = open(cf_fn, 'w')
        json.dump(cf, fw)
        fw.close()


    def parent_path(self, path):
        pars = path.split('/')
        return '/'.join(pars[:-1])

    def put(self, device, main_path, relate_path):
        device_host, device_ip = self.device_list[device]
        main_path = self.paths[main_path]
        path1 = "/home/"+self.host+'/'+main_path+"/"+relate_path
        path2 = "/home/"+device_host+'/'+main_path+"/"+relate_path
        path2 = self.parent_path(path2)

        cmd = "scp -r %s %s@%s:%s"%(path1, device_host, device_ip, path2)
        print(cmd)
        os.system(cmd)

    def put2(self, device, path1, path2):
        device_host, device_ip = self.device_list[device]
        if './' in path1:
            path1 = path1
        elif '/home' in path1:
            path1 = path1
        else:
            path1 = "/home/"+self.host+'/'+path1
        if '/home' in path2:
            path2 = path2
        else:
            path2 = "/home/"+device_host+'/'+path2
        path2 = self.parent_path(path2)

        cmd = "scp -r %s %s@%s:%s"%(path1, device_host, device_ip, path2)
        print(cmd)
        os.system(cmd)

    def get(self, device, main_path, relate_path):
        device_host, device_ip = self.device_list[device]
        main_path = self.paths[main_path]
        path1 = "/home/"+self.host+'/'+main_path+"/"+relate_path
        path2 = "/home/"+device_host+'/'+main_path+"/"+relate_path
        path1 = self.parent_path(path1)
        
        cmd = "scp -r %s@%s:%s %s"%(device_host, device_ip, path2, path1)
        print(cmd)
        os.system(cmd)

    def get2(self, device, path1, path2):
        device_host, device_ip = self.device_list[device]
        if './' in path1:
            path1 = path1
        elif '/home' in path1:
            path1 = path1
        else:
            path1 = "/home/"+self.host+'/'+path1
        if '/home' in path2:
            path2 = path2
        else:
            path2 = "/home/"+device_host+'/'+path2
        path1 = self.parent_path(path1)
        
        cmd = "scp -r %s@%s:%s %s"%(device_host, device_ip, path2, path1)
        print(cmd)
        os.system(cmd)
    
    def change_device(self, device, device_host, device_ip):
        self.device_list[device] = [device_host, device_ip]
        self.cf['device_list'] = self.device_list
        self.save_config(self.cf, self.cf_fn)
    
    def change_path(self, path_key, path):
        self.paths[path_key] = path
        self.cf['paths'] = self.paths
        self.save_config(self.cf, self.cf_fn)
    
    def login(self, device):
        device_host, device_ip = self.device_list[device]
        cmd = "ssh %s@%s"%(device_host, device_ip)
        print(cmd)
        os.system(cmd)
    
    def remove_pass(self, device, device_host, device_ip):
        cmd = "ssh-copy-id -i ~/.ssh/id_rsa.pub %s@%s"%(device_host, device_ip)
        print(cmd)
        os.system(cmd)
        self.change_device(device, device_host, device_ip)
    
    def cd(self, main_path):
        main_path = self.paths[main_path]
        path = "/home/"+self.host+'/'+main_path

        cmd = "cd %s"%(path)
        print(cmd)
        os.system(cmd)

    def disp_dic(self, dic):
        for key in dic:
            print(key, ':', dic[key])


# -- mian --
if (__name__ == "__main__"):
    argvs = sys.argv[1:]
    if len(argvs) == 0:
        argvs = ['-h']

    scpObj = SCP()
    if argvs[0] in ['put', 'send']:
        if len(argvs) == 1: scpObj.disp_dic(scpObj.device_list)
        if len(argvs) == 2: scpObj.disp_dic(scpObj.paths)
        if len(argvs) == 3: print(os.listdir( "/home/"+scpObj.host+'/'+scpObj.paths[argvs[2]]))
        if len(argvs) == 4:
            device = argvs[1]
            main_path = argvs[2]
            relate_path = argvs[3]
            scpObj.put(device, main_path, relate_path)
    if argvs[0] in ['put2', 'send2']:
        if len(argvs) == 1: scpObj.disp_dic(scpObj.device_list)
        if len(argvs) == 2: scpObj.disp_dic(scpObj.paths)
        if len(argvs) == 3: print(os.listdir( "/home/"+scpObj.host+'/'+scpObj.paths[argvs[2]]))
        if len(argvs) == 4:
            device = argvs[1]
            path1 = argvs[2]
            path2 = argvs[3]
            scpObj.put2(device, path1, path2)
    if argvs[0] in ['get']:
        if len(argvs) == 1: scpObj.disp_dic(scpObj.device_list)
        if len(argvs) == 2: scpObj.disp_dic(scpObj.paths)
        if len(argvs) == 3: print(os.listdir( "/home/"+scpObj.host+'/'+scpObj.paths[argvs[2]]))
        if len(argvs) == 4:
            device = argvs[1]
            main_path = argvs[2]
            relate_path = argvs[3]
            scpObj.get(device, main_path, relate_path)
    if argvs[0] in ['get2']:
        if len(argvs) == 1: scpObj.disp_dic(scpObj.device_list)
        if len(argvs) == 2: scpObj.disp_dic(scpObj.paths)
        if len(argvs) == 3: print(os.listdir( "/home/"+scpObj.host+'/'+scpObj.paths[argvs[2]]))
        if len(argvs) == 4:
            device = argvs[1]
            path1 = argvs[3]
            path2 = argvs[2]
            scpObj.get2(device, path1, path2)
    if argvs[0] in ['chd','change_device']:
        if len(argvs) == 1: scpObj.disp_dic(scpObj.device_list)
        if len(argvs) <  4: print("need input: device, device_host, device_ip")
        if len(argvs) == 4:
            device = argvs[1]
            device_host = argvs[2]
            device_ip = argvs[3]
            scpObj.change_device(device, device_host, device_ip)
    if argvs[0] in ['chp', 'change_path']:
        if len(argvs) == 1: scpObj.disp_dic(scpObj.paths)
        if len(argvs) == 3:
            path_key = argvs[1]
            path = argvs[2]
            scpObj.change_path(path_key, path)
    if argvs[0] in ['ln', 'login']:
        if len(argvs) == 1: scpObj.disp_dic(scpObj.device_list)
        if len(argvs) == 2:
            device = argvs[1]
            scpObj.login(device)
    if argvs[0] in ['rep', 'remove_pass']:
        if len(argvs) == 1: print("you need input the device")
        if len(argvs) == 2: print("you need input the device_host")
        if len(argvs) == 3: print("you need input the device_ip")
        if len(argvs) == 4:
            device, device_host, device_ip = argvs[1], argvs[2], argvs[3]
            scpObj.remove_pass(device, device_host, device_ip)
    if argvs[0] in ['cd']:
        if len(argvs) == 1: scpObj.disp_dic(scpObj.paths)
        if len(argvs) == 2:
            path = argvs[1]
            scpObj.cd(path)
    if argvs[0] == '-h' or argvs[0] == '--help':
        print("put: send the file from this machine to remote server.")
        print("put2: send the file from this machine to remote server.")
        print("get: get the file from remote server to this machine.")
        print("get2: get the file from remote server to this machine.")
        print("chd: change the device message(host_ip, user_name)")
        print("chp: change the path map")
        print("ln : login in the remote server")
        print("rep : remove the password of remote server")
        print("cd: as sh cd")
    
