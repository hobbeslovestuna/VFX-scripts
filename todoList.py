'''_________________
   vTodoList   : a simple TodoList widget for nuke to help organize your work
   author      : Victor Fleury
   version     : 0.1
'''
import os
from xml.etree import ElementTree as Etree
import nuke
from nukescripts import panels
from PySide.QtCore import *
from PySide.QtGui import *

class Task(object):

    _STATUS = ['TODO', 'WIP', 'FINISHED']

    def __init__(self, name, prio, amount):
        '''
            Init of the Task class.
            3 params :
                -_name
                -_priority
                -_amount done
        '''
        self._status = _STATUS[0]
        if not name == None and not prio == None:
            self._name      = name
            self._priority  = prio
            self._amount    = amount
        else:
            self._name      = ''
            self._priority  = 0
            self._amount    = 0

    def setName(self, name):
        '''
            Sets the name of the Task
        '''
        self._name = name

    def setPriority(self, prio):
        '''
            Sets the priority of the Task
        '''
        self._priority = prio

    def setStatus(self, status):
        if status in _STATUS :
            self._status = status
        else:
            return -1
    def __repr__(self):
        print 'Current task\n\tName :%s\n\tPriority :%i\n\t'

class TaskSaveAndLoad():
    '''
        Class to Save all the data regarding Tasks in XML and Read them.
    '''
    def __init__(self):
        if not nuke.Root()['project_directory'] == None:
            pass

class ToDoListUI(QWidget):
    '''
        The TodoList UI as a dockable widget
        Try to access it by a menu in the toolbar
    '''
    def __init__(self, parent = None):

        self._version   = '0.1'
        super(ToDoListUI, self).__init__(parent)
        
        self.layoutMain = QBoxLayout(QBoxLayout.TopToBottom, self)#.setLayout(QVBoxLayout)
        addTask_btn     = QPushButton('Add a task')
        showAllTask_btn = QPushButton('Show all task')

        rowLayout = QHBoxLayout()
        rowLayout.addWidget(addTask_btn)
        rowLayout.addWidget(showAllTask_btn)

        progress_bar = QProgressBar()

        self.layoutMain.addLayout(rowLayout)
        self.layoutMain.addWidget(progress_bar)

        #---
        #   Connextions
        #---
        self.connect(progress_bar, SIGNAL("clicked()"))
        self.show()

ui = ToDoListUI()
#panels.registerWidgetAsPanel('ToDoListUI', 'TodoList', 'fr.victor.ToDoListUI')