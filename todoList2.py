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
from functools import partial

class Task(dict):

    __STATUS = ['TODO', 'WIP', 'FINISHED']

    def __init__(self, name = None, status = 'TODO', progress = 0, priority = 0):
        '''
            Task Class
            Defines a task, will be used to create the UI
        '''
        super(Task, self).__init__()
        for key in ('name', 'status', 'progress',  'priority'):
            self[key] = ''
        if not name == None:
            self['name'] = name
        self['priority'] = priority
        self['progress'] = progress
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

    @property
    def progress(self):
        return self.get('progress', '')
    @progress.setter
    def progress(self, val):
        if not val in range(0,100):
            self['progress'] = 100
        else:
            self['progress'] = val

class TaskUI(QWidget):
    __STATUS = ['TODO', 'WIP', 'FINISHED']
    def __init__(self):
        super(TaskUI, self).__init__()

        # self.task            = None
        self.taskPriority    = 0
        self.taskStatus      = QComboBox()
        for statu in self.__STATUS:
            self.taskPriorityW.addItem(statu)

        self.taskLayout      = QHBoxLayout()
        self.taskName        = QLineEdit('Task name/description')
        self.taskPB          = TaskProgressBar()
        self.taskReset_btn   = QPushButton('Reset')
        self.taskRemove_btn  = QPushButton('Remove Task')

        self.taskLayout.addWidget(self.taskName)
        self.taskLayout.addWidget(self.taskPriorityW)
        self.taskLayout.addWidget(self.taskPB)
        self.taskLayout.addWidget(self.taskReset_btn)
        self.taskLayout.addWidget(self.taskRemove_btn)

        self.taskPB.reset()
        self.taskPB.left_clicked.connect(self.taskPB.update)
        self.taskPB.right_clicked.connect(self.taskPB.deupdate)
        self.taskReset_btn.clicked.connect(self.taskPB.reset)

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
        self.taskPriorityW.deleteLater()

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
        # saveAllTask_btn.clicked.connect(self.saveTodoList)
        # showAllTask_btn.clicked.connect(self.printTaskUI)

        self.show()

    def addTaskUI(self):
        '''
            Adds a layout being composed of a QLineEdit, a TaskProgressBar, and a button to reset the task
        '''
        taskUI = TaskUI()
        taskUI.taskRemove_btn.clicked.connect(partial(self.deleteTaskUI, taskUI))
        self.layoutMain.addLayout(taskUI.getLayout())
        self.allTasksUI.append(taskUI)
    
    def updateTaskUI(self):
        for i in self.allTasksUI:
            print i
    def deleteTaskUI(self, taskUI):
        taskUI.deleteTask()
        print 'test'
ui = ToDoListUI()