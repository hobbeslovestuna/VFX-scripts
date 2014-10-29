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
        Takes a task and stores it in the XML File
        Takes a XML file and retrieve all the tasks
    '''
    def __init__(self):
        if not nuke.Root()['project_directory'] == None:
            print nuke.Root()['project_directory'].value()
        else:
            print 'Not set'

class MyPB(QProgressBar):
    
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

        progressLayout      = QHBoxLayout()
        updateAmount_btn    = QPushButton('Reset')
        self.progress_bar   = MyPB()
        progressLayout.addWidget(self.progress_bar)
        progressLayout.addWidget(updateAmount_btn)

        self.layoutMain.addLayout(rowLayout)
        self.layoutMain.addLayout(progressLayout)
        # self.layoutMain.addWidget(progress_bar)

        #---
        #   Connections
        #---
        self.connect(updateAmount_btn, SIGNAL("clicked()"), self.reset)
        self.progress_bar.left_clicked.connect(self.update)
        self.progress_bar.right_clicked.connect(self.deupdate)
        self.progress_bar.dbl_clicked.connect(self.reset)
        self.show()

    def update(self):
        value = self.progress_bar.value()
        print value
        self.progress_bar.setValue(value + 10)
    def deupdate(self):
        value = self.progress_bar.value()
        self.progress_bar.setValue(value - 10)
    def reset(self):
        self.progress_bar.setValue(0)
ui = ToDoListUI()
#panels.registerWidgetAsPanel('ToDoListUI', 'TodoList', 'fr.victor.ToDoListUI')