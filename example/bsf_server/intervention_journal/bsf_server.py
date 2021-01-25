#!/usr/bin/env python3
# encoding: utf-8

import os
import sys
import time
import logging
import datetime
import pickle

from logging.handlers import RotatingFileHandler

import argparse
import configparser

import npyscreen

import django
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import base64, json, math
from simplecrypt import encrypt, decrypt


# there is some  import module after determining the sys.path

# minimum lines && column ( Termux for android)
MINIMUM_LINES=32
MINIMUM_COLUMNS=55

def configRead(sel,configName):
    #*******************************************************************
    #* function for read the ini file
    #*******************************************************************

    config = configparser.ConfigParser()
    config.read(configName)
    env= sel
    return config[env],env


# we can use global variable but i dont like it
# using a singleton instead for passing data in login form
class DataAccessLoginData:
    # Act like a singleton ( one object alone in all the code)
    instance = None
    def __init__(self):
        if not DataAccessLoginData.instance:
            DataAccessLoginData.instance=DataAccessCoreLoginData()

    def __getattr__(self, name):
        return getattr(self.instance, name)


class DataAccessCoreLoginData:

    def __init__(self) :
        self.userpasswordpath=None
        self.dataDecrypt = None

    def setwLogin(self,wl):
        self.wLogin = wl

    def setwPassword(self,wp):
        self.wPassword=wp

    def getUserPasswordPath(self):
        return self.userpasswordpath

    def setUserPasswordPath(self,userpasswordpath):
        self.userpasswordpath=userpasswordpath

    def setwLabel(self,wLabel):
        # widget message
        self.wLabel = wLabel

    def getwLabel(self):
        # widget message
        return self.wLabel

    def getForm(self):
        # login form
        return self.form

    def setForm(self,form):
        self.form = form

    def loginForOpeningSecret(self):

        #*******************************************************************
        #* Function for retrieving secret _key and decrypt_key per user
        #* Authenticate the password
        #*******************************************************************

        logger.info("loginForOpeningSecret")
        login = self.wLogin.value
        password = self.wPassword.value

        with open(self.userpasswordpath, 'rb') as f:
            userList = pickle.load(f)
        f.close()

        for userLine in userList :
            if login == userLine["login"] :
                try:
                    line = decrypt(password, userLine['cryptline'])
                    listLine = eval(line)
                    datadecrypt={}
                    datadecrypt["login"]=login
                    # ~ datadecrypt["password"]=password
                    datadecrypt["cryptline"]=line
                    datadecrypt["secret_key"]=listLine[0]
                    datadecrypt["cryptography_key"]=listLine[1]
                    logger.info("ok")
                    self.dataDecrypt = datadecrypt
                    return True
                except:
                    logger.info("password error for {}".format(login))
                    self.wLabel.value='erreur de mot de passe'
                    self.dataDecrypt = None
                    return False
        logger.info("login error for {}".format(login))
        self.wLabel.value='erreur de login'
        return False

    def getDataDecrypt(self):
        return self.dataDecrypt
    def setDataDecrypt(self,ddc):
        self.dataDecrypt = ddc


class OkLoginButton(npyscreen.ButtonPress):
    def __init__(self, *args, **keywords):
            super(npyscreen.ButtonPress, self).__init__(*args, **keywords)
            self.when_pressed_function=self.whenPressed
            self.name = "Ok"

    def whenPressed(self):
        # Launch the test login  and decrypt the data
        dataAccessLoginData = DataAccessLoginData()
        ok=dataAccessLoginData.loginForOpeningSecret()
        form = dataAccessLoginData.getForm()
        if ok == True :
            form.editing = False
        else:
            form.display()

def loginFrom(*listarg,**dictargs):

    # Create a form in the terminal with login / pawword
    F = npyscreen.Form(name='Login')
    wLogin  = F.add(npyscreen.TitleText, name = "Login:",)
    wPwd  = F.add(npyscreen.TitlePassword, name = "Mot de passe:",)
    F.nextrely +=1
    F.nextrelx +=2
    wok  = F.add(OkLoginButton)
    F.nextrely +=1
    wLabel  = F.add(npyscreen.FixedText, name = "",color='DANGER')

    # send data and object to the Button
    dataAccessLoginData = DataAccessLoginData()
    # store in singleton
    # here the value is none for now
    dataAccessLoginData.setwLogin(wLogin)
    dataAccessLoginData.setwPassword(wPwd)
    dataAccessLoginData.setwLabel(wLabel)
    dataAccessLoginData.setForm(F)
    F.edit()
    return None

class TerminalApplication(npyscreen.NPSAppManaged):
    #*******************************************************************
    #* Main Application
    #*
    #*******************************************************************

    def __init__(self):
        super().__init__()
        self.useEncrypt = False

    def onStart(self):
        form=self.registerForm("MAIN",Bsf_serverForm(minimum_lines=MINIMUM_LINES, minimum_columns=MINIMUM_COLUMNS) )

        # <bss_App>
        self.registerForm('INTERVENTIONSIMPLE',InterventionSimpleForm(minimum_lines=MINIMUM_LINES, minimum_columns=MINIMUM_COLUMNS) )
        self.registerForm('INTERVENTIONLIST',InterventionListForm(minimum_lines=MINIMUM_LINES, minimum_columns=MINIMUM_COLUMNS) )
        self.registerForm("INTERVENTIONEDIT",InterventionEditForm(minimum_lines=MINIMUM_LINES, minimum_columns=MINIMUM_COLUMNS) )
        self.registerForm('INTERVENTIONTREEVIEW',InterventionTreeviewForm(minimum_lines=MINIMUM_LINES, minimum_columns=MINIMUM_COLUMNS) )
        # </bss_App>

        contextjournal = ContextAccess()
        # <bsf_ChilParentRelation>
        contextjournal.addChildParentRelation('MAIN','App','INTERVENTIONSIMPLE')
        contextjournal.addChildParentRelation('INTERVENTIONSIMPLE','List','INTERVENTIONLIST')
        contextjournal.addChildParentRelation('INTERVENTIONSIMPLE','Treeview','INTERVENTIONTREEVIEW')
        contextjournal.addChildParentRelation('INTERVENTIONLIST','Edit','INTERVENTIONEDIT')
        contextjournal.addChildParentRelation('INTERVENTIONTREEVIEW','Edit','INTERVENTIONEDIT')
        # <bsf_ChilParentRelation>

        contextjournal.setMainApplication(ca)
        contextjournal.setMainFormName('MAIN')
        contextjournal.setCurrentFormName('MAIN')


        wf= self.getForm("MAIN")
        # ~ # set data for this specific application
        wf.setApplicationFORMAPP('journal','MAIN')


if __name__=="__main__":

    # retrieve path
    scriptdir = os.path.dirname( os.path.abspath(sys.argv[0]))

    # You launch from directory where manage.py exist or you are using settingpath argument
    launchdir = os.getcwd()
    pathname =os.path.abspath(launchdir)

    print("go to {} directory".format(pathname))

    # go to the directory
    os.chdir(pathname)

    # create parser
    parser = argparse.ArgumentParser()

    # add arguments to the parser
    parser.add_argument('-i', help='path and name to ini file. if not default is name of the script in the same directory')
    parser.add_argument('--projectpath', help='Django Application path directory where manage.py is placed')

    # parse the arguments
    args = parser.parse_args()

    # get the arguments value
    if args.projectpath != None:
        projectpath =os.path.abspath(args.projectpath)
        sys.path.append(args.projectpath)
    else:
        sys.path.insert(0,pathname)

    # load ini file
    if args.i != None:
        ini_filename = args.i
    else:
        script_file_name =  os.path.basename(sys.argv[0])
        script_corename=script_file_name.split('.py')[0]
        ini_filename = scriptdir+ os.sep + script_corename +'.ini'

    ini_filename = os.path.abspath(ini_filename)
    print("using {} as ini file".format(ini_filename))

    defaultini,env=configRead('DEFAULT',ini_filename)

    projectname = defaultini.get('projectname')
    applicationname = defaultini.get('applicationname')
    absolutelogpath=defaultini.get('absolutelogpath')
    logfile = defaultini.get('logfile')

    if absolutelogpath.upper() in ['YES','Y']:
        logfile = os.path.abspath(logfile)
    else:
        logfile = os.path.abspath(scriptdir + os.sep + logfile)

    weightlogfile = int(defaultini.get('weightlogfile'))
    numberofcyclelogfile = int(defaultini.get('numberofcyclelogfile'))

    exportdir=defaultini.get('exportdir')
    absoluteexportfile=defaultini.get('absoluteexportdir')

    if absoluteexportfile.upper() in ['YES','Y']:
        exportdir = os.path.abspath(exportdir)
    else:
        exportdir = os.path.abspath(scriptdir + os.sep + exportdir)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{}.settings".format(projectname))

    # logger object
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # formatting the log line
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    #  handler wich will write the log
    #  file in apend mode with a backup every 10Mo
    file_handler = RotatingFileHandler(logfile, 'a',weightlogfile,numberofcyclelogfile)
    #
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    encryptModule = defaultini.get('encryptModule')
    if encryptModule.upper() in ['YES','Y']:

        #*******************************************************************
        #* login / password form
        #*
        #*******************************************************************


        absoluteuserpassword=defaultini.get('absolutepathforuserpasswordfile')
        userpasswordfile = defaultini.get('userpasswordfile')
        if absoluteuserpassword.upper() in ['YES','Y']:
            userpasswordpath = os.path.abspath(userpasswordfile)
        else:
            userpasswordpath = os.path.abspath(scriptdir + os.sep + userpasswordfile)

        # data are encrypted in a pickle file
        dataAccessLoginData = DataAccessLoginData()
        dataAccessLoginData.setUserPasswordPath(userpasswordpath)

        npyscreen.wrapper_basic(loginFrom)

        dataDecrypt = dataAccessLoginData.getDataDecrypt()

        if dataDecrypt ==None:
            print ("Error login ")
            exit(1)
        secret_key=dataDecrypt["secret_key"]
        cryptography_key=dataDecrypt["cryptography_key"]

        # add the secret key
        settings.SECRET_KEY=secret_key
        settings.CRYPTOGRAPHY_KEY=cryptography_key
        # destroy the object
        dataAccessLoginData.setDataDecrypt(None)
        del dataDecrypt

    django.setup()

    #*******************************************************************
    #* test if we can access the model
    #*
    #*******************************************************************

    from journal.models import Intervention_Journal
    import lib.helper.helperModel
    helperModel = lib.helper.helperModel.HelperModel()

    print(helperModel.fields(Intervention_Journal))
    logger.info("fileds of Intervention_Journal")
    logger.info(helperModel.fields(Intervention_Journal))


    #*******************************************************************
    #* Django standalone is started launch the form
    #*
    #*******************************************************************

    from lib.ui.bsf_serverForm import Bsf_serverForm
    from journal.models import Intervention_Journal


    # <bss_ImportForm>
    from lib.intervention.ui.simple.interventionSimpleForm import InterventionSimpleForm
    from lib.intervention.ui.list.interventionListForm import InterventionListForm
    from lib.intervention.ui.edit.interventionEditForm import InterventionEditForm
    from lib.intervention.ui.treeview.interventionTreeviewForm import InterventionTreeviewForm
    # <bss_ImportForm>
    from lib.context.journalContextAccess import ContextAccess

    contextjournal = ContextAccess()
    contextjournal.setPathDirectoryExportFile(exportdir)

    # start of the log
    logger.info('Starting')
    logger.info(pathname)


    # create the Application for the login Form
    ca = TerminalApplication()
    ca.run()

    # go to initial directory
    os.chdir(launchdir)
    logger.info('End')
