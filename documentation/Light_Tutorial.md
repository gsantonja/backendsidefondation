*Ligth tutorial*
================

Path
====

You will find this example application in the directory /example/bsf_server

Actions
=======

*all your action need to be done in your django project directory*
> the django project directory is the project

*You want to create a new project :*

    django-admin startproject bsf_server
*You want to create a new application*

    python manage.py startapp journal

*Don't forget to parameter settiggs.py*

    add journal in INSTALLED_APPS

*create a table in journal.models.py*

like that :

    from django.utils.timezone import now

    class Intervention_Journal(models.Model):
        # class test for testing the skeleton template
        # those fields are needed to test the functionnality
        ticket =  models.CharField(max_length=100,default='',null=True,blank=True)
        comment =  models.CharField(max_length=200,default='',null=True,blank=True)
        update = models.DateTimeField(default = now,null=False)
        create = models.DateTimeField(default = now,null=False)

        def __str__(self):
            return "{} - {} - {}".format(self.update.strftime("%Y-%m-%d %H:%M:%S"),self.ticket)

*create the database*

	python manage.py makemigrations
	python manage.py migrate

*modify replaceApplication.ini*
In replaceApplication.ini file change the  `myProjectName` parameter
	
	myProjectName=bsf_server

Create [Intervention] label

`  [Intervention]`
`    MyComponent=intervention`
`    applicationName=journal`
`    dataElementName=interv`

`    modelClassName=Intervention_Journal`
`    MyApplication=bsf_server`

*make a directory in bsf_server like intervention_journal*

    mkdir intervention_journal

*launch replaceApplication.py*

	python ../backendSideFondation/fondation/tools/replaceInApplication.py -i ../backendSideFondation/fondation/tools/replaceInApplication.ini  -c Intervention -d ./intervention_journal

*launch the application*

	python intervention_journal/bsf_server.py

*and .. you have errors because you need to change the data and some customization*

	change the file ./intervention_journal/lib/customization/crud

*in InterventionCRUD.py change fromToData, fromToString, fromlist_all_Intervention_Journalfilter*

    def fromToData(self,interv,intervValue): if "id" in intervValue :
        interv.id = int(intervValue["id"]) if "ticket" in intervValue :
        interv.ticket = intervValue["ticket"] if "comment" in
        intervValue : interv.comment = intervValue["comment"] if
        "create" in intervValue : interv.create =
        datetime.strptime(intervValue["create"],"%Y-%m-%d %H:%M:%S" ) if
        "update" in intervValue : interv.update = now() return interv

    def fromToString(self,interv):
        intervValue={}
        intervValue["id"]=interv.id
        intervValue["ticket"]=interv.ticket
        intervValue["comment"]=interv.comment if interv.comment !=None else ""
        intervValue["update"]="{}".format(interv.update.strftime("%Y-%m-%d %H:%M:%S"))
        intervValue["create"]="{}".format(interv.create.strftime("%Y-%m-%d %H:%M:%S"))
        return intervValue

    def fromlist_all_Intervention_Journalfilter(self):
        # return the choice in filtering request
        filter_Intervention_Journal=["-update"]
        return filter_Intervention_Journal


*in InterventionEditCustomization.py change from_init_InterventionEditFormUI and from_calculer_editform*

    def from_init_InterventionEditFormUI(self,CancelButton , SaveButton):
        # it 's define the ui'
        ui=[]
        wd=[]
        ui.append("          1         2         3         4         5     ")
        ui.append(" 123456789012345678901234567890123456789012345678901234 ")
        ui.append("********************************************************")
        ui.append("*   BBBBBBBBBB   BBBBBBBBBB                            *")
        wd.extend([    CancelButton,SaveButton,])
        ui.append("*                                                      *")
        ui.append("*   RRRRRRRRRRRRRRRRRRRRRR                             *")
        wd.extend([    "title", ])
        ui.append("*                                                      *")
        ui.append("*   LLLLLLLLLLLLLLLLLL DDDDDDDDDD                      *")
        wd.extend(    ["Ticket           : ","ticket", ])
        ui.append("*   LLLLLLLLLLLLLLLLLL                                 *")
        wd.extend(   ["Comment         : ",])
        ui.append("*   DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD    *")
        wd.extend(   ["comment",])
        ui.append("*   LLLLLLLLLLLLLLLLL DDDDDDDDDDDDDDDDDDDD             *")
        wd.extend(   ["create          : ", "create",])
        ui.append("*   LLLLLLLLLLLLLLLLL DDDDDDDDDDDDDDDDDDDD             *")
        wd.extend(   ["update          : ", "update"])
        ui.append("*                                                      *")
        ui.append("*                                                      *")
        ui.append("*                                                      *")
        ui.append("*                                                      *")
        ui.append("*                                                      *")
        ui.append("*                                                      *")
        ui.append("*                                                      *")
        ui.append("*                                                      *")
        ui.append("********************************************************")

        # prepare the data
        ui.remove("          1         2         3         4         5     ")
        ui.remove(" 123456789012345678901234567890123456789012345678901234 ")
        ui.remove("********************************************************")
        ui.remove("********************************************************")
        ui1 = ["",]
        for line in ui :
         line = line[1:-1]
         ui1.append(line)
        ui = ui1

        # serialised description try to have he same organisation
        uiWdg= wd

        dictComboValue = {}

        # test if its ok
        helperUI =HelperUI(None)
        validateCompoWidget,isvalidated = helperUI.Analyse_UI(ui,uiWdg,dictComboValue,doCreateWidget=False)
        if isvalidated == "Yes" :
            logger.info(validateCompoWidget)
            return ui,uiWdg,dictComboValue
        else:
            logger.error(isvalidated)
            logger.error(validateCompoWidget)
            raise FillRuleError(isvalidated)

    def from_calculer_editform(self,interv,allValueInEditForm):
        resultCalculate = {}
        resultCalculate["title"]="{}-{}".format(interv.id,allValueInEditForm["ticket"])
        return resultCalculate

*in interventionSimpleCustomization.py change from_on_reservation1,from_init_InterventionSimpleFormUI*

    def from_on_reservation1(self,values):
        resultCalculate = {}
        return resultCalculate


    def from_init_InterventionSimpleFormUI(self):

      InterventionToListButton = self.contextAccess.getButtonClass('InterventionToListButton')
      MainAppButton  = self.contextAccess.getButtonClass('MainButton')
      ExitButton = self.contextAccess.getButtonClass('ExitButton')

       # GUI form column 0 to column 54
       # from line 2 (next to empty first line
       # L = label
       # B = Button
       # V = Value
       wd=[]
       ui=[]
       ui.append("          1         2         3         4         5     ")
       ui.append(" 123456789012345678901234567890123456789012345678901234 ")
       ui.append("********************************************************")
       ui.append("*   LLLLLLLLLLLLLLL                                    *")
       wd.extend([   "Intervention : "])
       ui.append("*                                                      *")
       ui.append("*   LLLLLLLLLLLL     BBBBBBBBBB                        *")
       wd.extend([    "List    : ", InterventionToListButton])
       ui.append("*                                                      *")
       ui.append("*                                                      *")
       ui.append("*   LLLLLLLLLLLL     BBBBBBBBBB                        *")
       wd.extend([   "Main    : ",MainAppButton])
       ui.append("*                                                      *")
       ui.append("*                                                      *")
       ui.append("*   BBBBBBB                                            *")
       wd.extend([    ExitButton])
       ui.append("*                                                      *")
       ui.append("*                                                      *")
       ui.append("*                                                      *")
       ui.append("*                                                      *")
       ui.append("*                                                      *")
       ui.append("*                                                      *")
       ui.append("*                                                      *")
       ui.append("*                                                      *")
       ui.append("*                                                      *")
       ui.append("*                                                      *")
       ui.append("********************************************************")


       # prepare the data
       ui.remove("          1         2         3         4         5     ")
       ui.remove(" 123456789012345678901234567890123456789012345678901234 ")
       ui.remove("********************************************************")
       ui.remove("********************************************************")
       ui1 = [""]
       for line in ui :
          line = line[1:-1]
          ui1.append(line)
       ui = ui1

       # serialised description try to have he same organisation
       uiWdg= wd

       # test if its ok
       helperUI =HelperUI(None)
       validateCompoWidget,isvalidated = helperUI.Analyse_UI(ui,uiWdg,{},doCreateWidget=False)
       if isvalidated == "Yes" :
           logger.info(validateCompoWidget)
           return ui,uiWdg,{}
       else:
           logger.error(isvalidated)
           logger.error(validateCompoWidget)
           raise FillRuleError(isvalidated)

*Launch the application*
launch

python ./intervention_journal/bsf_server.py


