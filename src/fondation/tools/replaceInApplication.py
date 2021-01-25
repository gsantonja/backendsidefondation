#!/usr/bin/env python3
# encoding: utf-8
import os
import sys
import configparser
import shutil
import argparse
import logging
import pprint
from logging.handlers import RotatingFileHandler

#*******************************************************************
#* Script for translate the
#* function for read the ini file
#* function for read the ini file
#*******************************************************************



def configRead(sel,configName):
    #*******************************************************************
    #* function for read the ini file
    #*******************************************************************

    config = configparser.ConfigParser()
    config.read(configName)
    env= sel
    return config[env],env

# ~ replace string in py file for changing the name of class and switch between Form
# ~ from previous form

def replaceInfile(filein,fileout,dictreplace):
    # open file reading
    print ("traitemnt de {}".format(filein))
    if os.path.exists(fileout):
        shutil.copyfile(fileout,fileout+".sav")

    f = open(filein,'r')
    filedata = f.read()
    f.close()
    #change data
    for k,v in dictreplace.items():
        if filedata.count(k) != 0 :
            # ~ print (" {} occurence(s) de {} ".format(filedata.count(k),k))
            # ~ print ("replace {} by {} ".format(k,v))
            filedata = filedata.replace(k,v)

    # save file
    f= open(fileout,'w')
    f.write(filedata)
    f.close()

    # the proces end well
    if os.path.exists(fileout+".sav"):
        os.remove(fileout+".sav")

def replaceInfile(filein,fileout,dictreplace):
    # open file reading
    print ("traitemnt de {}".format(filein))
    if os.path.exists(fileout):
        shutil.copyfile(fileout,fileout+".sav")

    f = open(filein,'r')
    filedata = f.read()
    f.close()
    #change data
    for k,v in dictreplace.items():
        if filedata.count(k) != 0 :
            # ~ print (" {} occurence(s) de {} ".format(filedata.count(k),k))
            # ~ print ("replace {} by {} ".format(k,v))
            filedata = filedata.replace(k,v)

    # save file
    f= open(fileout,'w')
    f.write(filedata)
    f.close()

    # the proces end well
    if os.path.exists(fileout+".sav"):
        os.remove(fileout+".sav")

def replaceInString(stringin,dictreplace):
    stringout =stringin
    for k,v in dictreplace.items():
        # ~ print (k,v)
        if stringout.count(k) != 0 :
            # ~ print (" {} occurence(s) de {} ".format(stringout.count(k),k))
            # ~ print ("replace {} by {} ".format(k,v))
            stringout = stringout.replace(k,v)
    return stringout

if __name__=="__main__":

    # retrieve path
    scriptdir = os.path.dirname( os.path.abspath(sys.argv[0]))
    launchdir = os.getcwd()
    pathname =os.path.abspath(scriptdir+os.sep + '..')

    # create parser
    parser = argparse.ArgumentParser()

    # add arguments to the parser
    parser.add_argument('-i', help=' ini file')
    parser.add_argument('-d', help=' path to target directory ')
    parser.add_argument('-c', help=' name of the componet defined in ini file ')
    # parse the arguments
    args = parser.parse_args()

    # get the arguments value
    if args.i != None:
        ini_filename = args.i
    else:
        script_file_name =  os.path.basename(sys.argv[0])
        script_corename=script_file_name.split('.py')[0]
        ini_filename = scriptdir+ os.sep + script_corename +'.ini'

    ini_filename = os.path.abspath(ini_filename)
    print("using {} as ini file".format(ini_filename))

    if args.d != None:
        dirname = args.d
        if os.path.abspath(pathname) != dirname :
            if os.path.isdir(dirname)==False:
                # relative path name the chg dir break it
                dirname = os.path.abspath(launchdir + os.sep + dirname)
                if os.path.isdir(dirname)==False:
                    print("can't find directory try aboslute path")
                    sys.exit(1)
            else:
                dirname = os.path.abspath(dirname)
    else:
        print("ereur imprevue dans arg parse???")
        sys.exit(1)

    if args.c != None:
        componentParameter = args.c
    else:
        print("ereur imprevue dans arg parse???")
        sys.exit(1)

    defaultini,env=configRead('DEFAULT',ini_filename)


    # add directory out of "console" wich contain djangoo app
    # the chdir break relative path in parameter
    os.chdir(pathname)
    sys.path.insert(0,pathname)

    # project Name
    projectnameTarget= defaultini.get('myProjectName')
    projectnameSource= defaultini.get('projectNameFrom')

    # encryptModule Yes /No
    encryptModule= defaultini.get('encryptModule')



    # the main application file
    pathMainFilePyFrom=defaultini.get('pathMainFilePyFrom')
    pathMainFileIniFrom=defaultini.get('pathMainFileIniFrom')

    # load file path from
    pathmain= defaultini.get('pathMainFrom')
    pathlibcomefrom =   defaultini.get('pathLibFrom')

    # Load strind to replace using [Fondation]
    fondationini,env1=configRead('Fondation',ini_filename)
    componentFondation= fondationini.get('componentFondation')
    componentDataElementName= fondationini.get('componentDataElementName')
    componentModelClassName= fondationini.get('componentModelClassName')
    componentApplicationName = fondationini.get('componentApplicationName')
    componentMyApplication = fondationini.get('componentMyApplication')

    lineImportModelSource= fondationini.get('lineImportModelSource')
    lineImportModelTarget= fondationini.get('lineImportModelTarget')

    # Load strind to replace using [componentParameter]
    componentini,env1=configRead("{}".format(componentParameter),ini_filename)
    myComponent = componentini.get("MyComponent")
    dataElementName = componentini.get("dataElementName")
    modelClassName  = componentini.get("modelClassName")
    applicationName = componentini.get("applicationName")
    myApplication = componentini.get("MyApplication")

    dictreplaceInit = {}
    dictreplaceInit[componentFondation]=myComponent
    dictreplaceInit[componentDataElementName]=dataElementName
    dictreplaceInit[componentModelClassName]=modelClassName
    dictreplaceInit[componentApplicationName]=applicationName
    dictreplaceInit[componentMyApplication]=myApplication

    # create the data reference with key to be replaced
    dictreplace = {}
    # add line that need to replace
    dictreplace[lineImportModelSource]=lineImportModelTarget
    # add fistUpper and Upper string
    for key, val in  dictreplaceInit.items():
        dictreplace[key]=val
        # first upper
        keyFu="{}{}".format(key[0].upper(),key[1:])
        valFu="{}{}".format(val[0].upper(),val[1:])
        dictreplace[keyFu]=valFu
        # upper
        keyU=key.upper()
        valU=val.upper()
        dictreplace[keyU]=valU
        print(valU,keyU)
        print(valFu,keyFu)

    # information if you want to preserve you customize file
    erase_all = defaultini['erase_all']
    preserve_crud_class = defaultini['preserve_crud_class']
    preserve_business_rule_class = defaultini['preserve_business_rule_class']
    preserve_uicustom_class = defaultini['preserve_uicustom_class']

    # log file
    logfile = defaultini['logfile']
    weightlogfile = int(defaultini['weightlogfile'])
    numberofcyclelogfile = int(defaultini['numberofcyclelogfile'])


    # create file log
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # format the log line
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    # handler with a second file in backup
    file_handler = RotatingFileHandler(logfile, 'a',weightlogfile,numberofcyclelogfile)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # second handler for the console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    logger.addHandler(stream_handler)

    dirname = dirname + os.sep

    logger.info('Start')
    logger.info(dirname)

    print(dirname)
    pprint.pprint(dictreplace)
    pathmaincomeout = replaceInString(os.path.join(dirname,pathMainFilePyFrom),dictreplace)
    replaceInfile(os.path.join(pathmain,pathMainFilePyFrom),pathmaincomeout,dictreplace)
    print("cible {} ".format(pathmaincomeout))


    # replace in ini file add projectname line
    # and encrypt line
    source="projectname={}".format(projectnameSource)
    target="projectname={}".format(projectnameTarget)

    # encrypt module = Yes by default
    encryptModuleSource="encryptModule=Yes"
    encryptModuleTarget="encryptModule={}".format(encryptModule)


    dictreplace1 = dictreplace.copy()
    dictreplace1[source]=target
    dictreplace1[encryptModuleSource]=encryptModuleTarget

    pathmaincomeout = replaceInString(os.path.join(dirname,pathMainFileIniFrom),dictreplace)
    replaceInfile(os.path.join(pathmain,pathMainFileIniFrom),pathmaincomeout,dictreplace1)

    pathlibcomefrom = os.path.abspath(os.path.join(pathmain,pathlibcomefrom)) + os.sep
    print ("pathlibcomefrom {}".format(pathlibcomefrom))

    for root, directories, files in os.walk(pathlibcomefrom, topdown=True):
        # ~ print (root)
        # ~ print (directories)
        # ~ print(files)
        # need to check directory first
        for d in directories :
            if "__pycache__" in d :
                pass
                logger.info("__pycache__ ignoré " + os.path.join(dirname,d))
                # ~ print ("cache")
            else:
                # ~ if os.path.isdir(os.path.join(dirname,d))==False:
                    # ~ print (d)
                    # ~ print ("makedir {}".format(os.path.join(dirname,d)))
                    # ~ os.makedirs(os.path.join(dirname,d), exist_ok=True)

                for filename in os.listdir(os.path.join(root,d)):
                    if os.path.isfile(os.path.join(root,d, filename)):
                        f=os.path.basename(filename)
                        # ~ print("extraction {}".format(f[-3:]))
                            # for now do nothing. may change
                        if f[-3:] == ".py" :
                            # only *.py file
                            doNotTouch=False
                            name = componentParameter
                            # search for string to replace and preserve data specific
                            if erase_all not in ["Yes",'Y'] and preserve_crud_class in ["Yes",'Y'] :
                                fsearch=replaceInString(f,dictreplace)
                                nameupper= "CRUD.py"
                                # ~ print(" <{}> vs <{}>".format(fsearch.upper(),nameupper))
                                if fsearch.upper() == nameupper :
                                    doNotTouch=True
                                    # ~ print("Exclusion de {}".format(fsearch))

                            if erase_all not in ["Yes",'Y'] and preserve_business_rule_class in ["Yes",'Y'] :
                                fsearch=replaceInString(f,dictreplace)
                                nameupper= "Rule.py".format(name).upper()
                                if fsearch.upper() == nameupper :
                                    doNotTouch=True
                                    # ~ print("Exclusion de {}".format(fsearch))

                            if erase_all not in ["Yes",'Y'] and preserve_uicustom_class in ["Yes",'Y'] :
                                fsearch=replaceInString(f,dictreplace)
                                listCustom=["SimpleCustomization.py","EditComboBoxCustomization.py"]
                                listCustom.append("EditCustomization.py")
                                listCustom.append("TreeViewCustomization.py")
                                listCustom.append("ListCustomization.py")

                                for  nameupper1 in listCustom:
                                    nameupper= "{}{}".format(name,nameupper1).upper()
                                    if fsearch.upper() == nameupper :
                                        doNotTouch=True
                                        # ~ print("Exclusion de {}".format(fsearch))


                            filepath= os.path.join(root,d,filename)
                            if doNotTouch==False:
                                filepath = os.path.abspath(filepath)
                                # ~ print(filepath)
                                # ~ print("dirname {}".format(dirname))
                                # ~ print("pathmain {}".format(pathmain))
                                filepathout=filepath.replace(pathmain,dirname)
                                pathlibcomeout = replaceInString(filepathout,dictreplace)
                                # create if doesnt exist
                                d1=os.path.dirname(pathlibcomeout)
                                os.makedirs(d1, exist_ok=True)
                                replaceInfile(os.path.join(root,d,filename),pathlibcomeout,dictreplace)
                                # ~ print ("creation de {}".format(pathlibcomeout))
                                logger.info("traitement de {}".format(filepath))
                            else:
                                print("[Exclusion] de {}".format(filepath))
                                logger.info("[Exclusion] de {}".format(filepath))
                        else :
                            pass


    # go to initial directory
    os.chdir(launchdir)
    logger.info('Fin')

