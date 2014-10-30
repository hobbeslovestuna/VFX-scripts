'''_________________
   vTodoList   : a simple TodoList widget for nuke to help organize your work
   author      : Victor Fleury
   version     : 0.1
'''
import os
#from xml.etree import ElementTree as Etree
import nuke
import json
from nukescripts import panels
from PySide.QtCore import *
from PySide.QtGui import *

class Task(dict):

    __STATUS = ['TODO', 'WIP', 'FINISHED']

    def __init__(self, name = None, prio = None, percent = 0):
        '''
            Init of the Task class.
            4 params :
                -name
                -priority
                -percent done
                -stauts
        '''
        super(Task, self).__init__()
        for key in ('name', 'priority', 'percent', 'status'):
            self[key] = ''
        if not name == None:
            self['name'] = name
        if not prio == None:
            self['priority'] = prio
        self['percent'] = percent
        self['status'] = self.__STATUS[0]

    @property
    def name(self):
        return self.get('name', '')

    @name.setter
    def name(self, val):
        self['name'] = val

    @property
    def priority(self):
        return self.get('priority', '')
    
    @priority.setter
    def priority(self, val):
        if isinstance(val, int):
            self['priority'] = val
        else:
            raise TypeError('The value you entered for the priority is not an int.')

    @property
    def status(self):
        return self.get('status', '')
    @status.setter
    def status(self, val):
        if not val in self.__STATUS:
            raise TypeError('The status does not belong to the list')
        else:
            self['status'] = val

    # def __repr__(self):
    #     return json.dumps(self, sort_keys = True, indent = 4)


class TaskSaveAndLoader(object):
    '''
        Class to Save all the data regarding Tasks in XML and Read them.
        Takes a task and stores it in the XML File
        Takes a XML file and retrieve all the tasks
    '''
    def __init__(self):
        self.__path = None
        if not nuke.Root()['name'] == None:
            # print nuke.Root()['name'].value()
            self.__path = os.path.split(nuke.Root()['name'].value())[0] + '/'
        else:
            self.__path = None
        print self.__path
    
    def loadTasks(self):
        '''
            loadTasks : Go fetch the json file which will have the name ToDoList.json
        '''
        if os.path.exists(self.__path):
            jsonFile = os.path.join(self.__path, 'ToDoList.json')
            jsonData = open(jsonFile, 'r')
            print json.load(jsonData)
            jsonData.close()
    
    def saveTask(self, Task):
        '''
            saveTask : Saves the task to the json file set with the path
        '''
        if os.path.exists(self.__path):
            jsonFile = os.path.join(self.__path, 'ToDoList.json')
            with open(jsonFile, 'w') as f:
                json.dump(Task, f, indent = 4)
        else:
            raise IOError('The file could not be written du to a wring path')

    def saveTasks(self, listTasks):
        jsonFile = os.path.join(self.__path, 'ToDoList.json')
        with open(jsonFile, 'w') as f:
            json.dump(task, f, indent = 4)
        f.close()



class TaskProgressBar(QProgressBar):
    
    left_clicked   = Signal()
    right_clicked  = Signal()
    dbl_clicked    = Signal()

    def __init__(self):
        QProgressBar.__init__(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print 'Left cliked emitted'
            self.left_clicked.emit()
        if event.button() == Qt.RightButton:
            print 'Right clicked emitted'
            self.right_clicked.emit()
        if event.button() == QEvent.MouseButtonDblClick:
            print 'Double click'
            self.dbl_clicked.emit()


class TaskUI(QWidget):

    def __init__(self):
        self.taskLayout      = QHBoxLayout()
        self.taskName        = QLineEdit('Task name/description')
        self.taskPB          = TaskProgressBar()
        self.taskReset_btn   = QPushButton('Reset')
        
        self.taskLayout.addWidget(self.taskName)
        self.taskLayout.addWidget(self.taskPB)
        self.taskLayout.addWidget(self.taskReset_btn)

        self.taskPB.reset()

        self.taskPB.left_clicked.connect(self.update)
        self.taskPB.right_clicked.connect(self.deupdate)

    def getLayout(self):
        return self.taskLayout

    def update(self):
        value = self.taskPB.value()
        print value
        self.taskPB.setValue(value + 10)
    def deupdate(self):
        value = self.taskPB.value()
        self.taskPB.setValue(value - 10)
    def reset(self):
        self.taskPB.setValue(0)

class ToDoListUI(QWidget):
    '''
        The TodoList UI as a dockable widget
        Try to access it by a menu in the toolbar
    '''
    def __init__(self, parent = None):

        self._version   = '0.1'
        super(ToDoListUI, self).__init__(parent)
        
        self.layoutMain = QBoxLayout(QBoxLayout.TopToBottom, self)#.setLayout(QVBoxLayout)
        addTask_btn       = QPushButton('Add a task')
        showAllTask_btn   = QPushButton('Show all task')

        rowLayout = QHBoxLayout()
        rowLayout.addWidget(addTask_btn)
        rowLayout.addWidget(showAllTask_btn)

        # progressLayout      = QHBoxLayout()
        # updatepercent_btn    = QPushButton('Reset')
        # self.progress_bar   = TaskProgressBar()
        # self.progress_bar.reset()
        # progressLayout.addWidget(self.progress_bar)
        # progressLayout.addWidget(updatepercent_btn)

        self.layoutMain.addLayout(rowLayout)
        # self.layoutMain.addLayout(progressLayout)
        # self.layoutMain.addWidget(progress_bar)

        #---
        #   Connections
        #---
        # self.connect(updatepercent_btn, SIGNAL("clicked()"), self.reset)
        addTask_btn.clicked.connect(self.addTaskUI)
        # self.progress_bar.left_clicked.connect(self.update)
        # self.progress_bar.right_clicked.connect(self.deupdate)
        # # self.progress_bar.dbl_clicked.connect(self.reset)
        self.show()

    def addTaskUI(self):
        '''
            Adds a layout being composed of a QLineEdit, a TaskProgressBar, and a button to reset the task
        '''
        taskUI = TaskUI()
        self.layoutMain.addLayout(taskUI.getLayout())
        

ui = ToDoListUI()
#panels.registerWidgetAsPanel('ToDoListUI', 'TodoList', 'fr.victor.ToDoListUI')