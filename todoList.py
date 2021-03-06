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
    def update(self):
        value = self.value()
        print value
        self.setValue(value + 10)

    def deupdate(self):
        value = self.value()
        self.setValue(value - 10)
    def reset(self):
        self.setValue(0)

class TaskUI(QWidget):

    def __init__(self, parent):
        super(TaskUI, self).__init__(parent)
        self.task            = None
        self.taskPriority    = 0
        self.taskLayout      = QHBoxLayout()
        self.taskName        = QLineEdit('Task name/description')
        self.taskPB          = TaskProgressBar()
        self.taskReset_btn   = QPushButton('Reset')
        self.taskRemove_btn  = QPushButton('Remove Task')
        
        self.taskLayout.addWidget(self.taskName)
        self.taskLayout.addWidget(self.taskPB)
        self.taskLayout.addWidget(self.taskReset_btn)
        self.taskLayout.addWidget(self.taskRemove_btn)

        self.taskPB.reset()

        self.taskPB.left_clicked.connect(self.taskPB.update)
        self.taskPB.right_clicked.connect(self.taskPB.deupdate)
        self.taskReset_btn.clicked.connect(self.taskPB.reset)
        self.taskRemove_btn.clicked.connect(ToDoListUI.printTaskUI)

    def getLayout(self):
        return self.taskLayout

    def getTaskFromUI(self):
        self.task = Task(self.taskName.text(), self.taskPriority, self.taskPB.value())
        #print self.task
        return self.task
    
    def deleteTask(self):
        print 'prout'
        self.taskName.deleteLater()
        self.taskPB.deleteLater()
        self.taskReset_btn.deleteLater()
        self.taskRemove_btn.deleteLater()
        self.taskLayout.deleteLater()

class ToDoListUI(QWidget):
    '''
        The TodoList UI as a dockable widget
        Try to access it by a menu in the toolbar
    '''
    def __init__(self, parent = None):

        super(ToDoListUI, self).__init__(parent)
        self._version       = '0.1'
        self.allTasksUI     = []
        
        self.layoutMain     = QBoxLayout(QBoxLayout.TopToBottom, self)#.setLayout(QVBoxLayout)
        addTask_btn         = QPushButton('Add a task')
        showAllTask_btn     = QPushButton('Show all task')
        saveAllTask_btn     = QPushButton('Save all tasks')

        rowLayout = QHBoxLayout()
        rowLayout.addWidget(addTask_btn)
        rowLayout.addWidget(saveAllTask_btn)
        rowLayout.addWidget(showAllTask_btn)


        self.layoutMain.addLayout(rowLayout)

        #---
        #   Connections
        #---
        addTask_btn.clicked.connect(self.addTaskUI)
        saveAllTask_btn.clicked.connect(self.saveTodoList)
        showAllTask_btn.clicked.connect(self.printTaskUI)

        self.show()

    def addTaskUI(self):
        '''
            Adds a layout being composed of a QLineEdit, a TaskProgressBar, and a button to reset the task
        '''
        taskUI = TaskUI(parent = self)
        self.layoutMain.addLayout(taskUI.getLayout())
        self.allTasksUI.append(taskUI)
        
    def saveTodoList(self, listTaskUI):
        # for i in list
        pass
    
    def printTask(self):
        for i in range(self.layoutMain.count()):
            sublayout = self.layoutMain.itemAt(i)
            for s in range(sublayout.count()):
                print type(sublayout.itemAt(s))
                print s

    def printTaskUI(self):
        for task in self.allTasksUI:
            print task.getTaskFromUI()

ui = ToDoListUI()
panels.registerWidgetAsPanel('ToDoListUI', 'TodoList', 'fr.victor.ToDoListUI')