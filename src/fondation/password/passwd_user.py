#!/usr/bin/env python3
# encoding: utf-8

import os
import sys
import configparser
import pickle

from simplecrypt import encrypt, decrypt


# there is some  import module after determining the sys.path

def configRead(sel,configName):
    #*******************************************************************
    #* function for read the ini file
    #*******************************************************************

    config = configparser.ConfigParser()
    config.read(configName)
    env= sel
    return config[env],env

if __name__=="__main__":
    # TODO : create a real script .
    # this script create a password file with one user

    # retrieve path
    scriptdir = os.path.dirname( os.path.abspath(sys.argv[0]))

    # You launch from directory where manage.py exist or you are using settingpath argument
    launchdir = os.getcwd()
    pathname =os.path.abspath(launchdir)

    print("go to {} directory".format(pathname))

    # go to the directory
    os.chdir(scriptdir)

    # retrieve ini information
    defaultini,env=configRead('DEFAULT',"passwd_user.ini")

    login=defaultini.get('login')
    password=defaultini.get('password')
    filepassword = defaultini.get('filepassword')
    secret_key=defaultini.get('secret_key')

    # if you lost the cryptographic key you will lost your data
    cryptography_key=defaultini.get('cryptography_key')

    # create pickle file
    userList1=[]
    userLine1={}
    # you can't decrypt ot much fiel because simplecrypt have a cooldown of 2s
    userLine1['cryptline']="['{}','{}']".format(secret_key,cryptography_key)
    userLine1['cryptline'] = userLine1['cryptline'].encode()
    userLine1['cryptline'] = encrypt(password, userLine1['cryptline'])
    userLine1['login']="{}".format(login)
    userList1.append(userLine1)

    # save the file
    with open(filepassword, 'wb') as f1:
        pickle.dump(userList1, f1)
    f1.close()
    print("fini")
    os.chdir(launchdir)

