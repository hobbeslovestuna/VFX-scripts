'''_________________
   vTodoList   : a simple TodoList widget for nuke to help organize your work
   author      : Victor Fleury
   version     : 0.2
'''
import os
import nuke
import json
from nukescripts import panels
from PySide.QtCore import *
from PySide.QtGui import *
from functools import partial

class Task(dict):

    __STATUS = ['TODO', 'WIP', 'FINISHED']

    def __init__(self, name = None, status = None, progress = 0, priority = 0):
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
        if not self['status'] == None:
           self['status'] = status
        else:
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
    '''
        TaskUI : a class that rperesent a Task using QWidgets
    '''
    __STATUS = ['TODO', 'WIP', 'FINISHED']
    def __init__(self, name = None, status = None, priority = None, progress = None):
        super(TaskUI, self).__init__()

        # self.task            = None
        self.taskPriority    = QComboBox()
        self.taskPriority.addItem('0')
        self.taskPriority.addItem('1')
        self.taskPriority.addItem('2')

        self.taskStatus      = QComboBox()
        for statu in self.__STATUS:
            self.taskStatus.addItem(statu)

        if not status == None:
            if status == self.__STATUS[0]:
                self.taskStatus.setCurrentIndex(0)
            elif status == self.__STATUS[1]:
                self.taskStatus.setCurrentIndex(1)
            else:
                self.taskStatus.setCurrentIndex(2)


        self.taskLayout      = QHBoxLayout()
        if not name == None:
            self.taskName = QLineEdit(str(name))
        else:
            self.taskName = QLineEdit('Task name/description')
        self.taskPB          = TaskProgressBar()
        self.taskReset_btn   = QPushButton('Reset')
        self.taskRemove_btn  = QPushButton('Remove Task')

        self.taskLayout.addWidget(self.taskName)
        self.taskLayout.addWidget(self.taskStatus)
        self.taskLayout.addWidget(self.taskPriority)
        self.taskLayout.addWidget(self.taskPB)
        self.taskLayout.addWidget(self.taskReset_btn)
        self.taskLayout.addWidget(self.taskRemove_btn)

        if not progress == None:
            self.taskPB.setValue(int(progress))
        else:
            self.taskPB.reset()
        self.taskPB.left_clicked.connect(self.taskPB.update)
        self.taskPB.right_clicked.connect(self.taskPB.deupdate)
        self.taskReset_btn.clicked.connect(self.taskPB.reset)
        self.taskStatus.currentIndexChanged.connect(self.updateStatus)

    def getLayout(self):
        return self.taskLayout

    def deleteTask(self):
        print 'prout'
        self.taskName.deleteLater()
        self.taskPB.deleteLater()
        self.taskReset_btn.deleteLater()
        self.taskRemove_btn.deleteLater()
        self.taskLayout.deleteLater()
        self.taskStatus.deleteLater()
        self.taskPriority.deleteLater()

    def updateStatus(self):
        print self.taskStatus.currentText()


class TaskProgressBar(QProgressBar):
    '''
        Implementation of our own QProgressBar to enable it to be clicked
    '''
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

class TaskSaveAndLoader(object):
    '''
        Class to Save all the data regarding Tasks in JSON and Read them.
        Takes a task and stores it in the JSON File
        Takes a JSON file and retrieve all the tasks
    '''
    def __init__(self):
        self.__path = None
        if not nuke.Root()['name'] == None:
            # print nuke.Root()['name'].value()
            self.__path = os.path.split(nuke.Root()['name'].value())[0] + '/'
        else:
            self.__path = None
        print self.__path
    
    def taskFileExist(self):
        if not self.__path == None:
            if os.path.exists(os.path.join(self.__path, 'ToDoList.json')):
                return True
        else:
            return False

    def loadTasks(self):
        '''
            loadTasks : Go fetch the json file which will have the name ToDoList.json
        '''
        if os.path.exists(self.__path):
            jsonFile = os.path.join(self.__path, 'ToDoList.json')
            jsonData = open(jsonFile, 'r')
            data = json.load(jsonData)
            jsonData.close()
            # os.unlink(jsonFile)
            self.__path = None
            return data
    
    def saveTask(self, Task):
        '''
            saveTask : Saves the task to the json file set with the path
        '''
        if os.path.exists(self.__path):
            jsonFile = os.path.join(self.__path, 'ToDoList.json')
            with open(jsonFile, 'w') as f:
                json.dump(Task, f, indent = 4)
            f.close()
            # os.unlink(f)
            self.__path = None
        else:
            raise IOError('The file could not be written du to a wring path')

    def saveTasks(self, listTasks):
        jsonFile = os.path.join(self.__path, 'ToDoList.json')
        with open(jsonFile, 'w') as f:
            json.dump(listTasks, f, indent = 4)
        f.close()
        self.__path = None

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

        self.tasksLayout = QVBoxLayout()

        self.layoutMain.addLayout(rowLayout)
        self.layoutMain.addLayout(self.tasksLayout)

        #---
        #   Connections
        #---
        addTask_btn.clicked.connect(self.addTaskUI)
        saveAllTask_btn.clicked.connect(self.saveTodoList)
        # showAllTask_btn.clicked.connect(self.printTaskUI)

        self.taskSaveAndLoader = TaskSaveAndLoader()
        if self.taskSaveAndLoader.taskFileExist():
            #Add tasks
            existingTasks = self.taskSaveAndLoader.loadTasks()
            for et in existingTasks:
                #print et['name']
                self.addTaskUI(et['name'], et['status'], et['priority'], et['progress'])
        # self.show()

    def addTaskUI(self, name = None, status = None, priority = None, progress = None):
        '''
            Adds a layout being composed of a QLineEdit, a TaskProgressBar, and a button to reset the task
        '''
        if name == None and status == None and priority == None and progress == None:
            taskUI = TaskUI()
            taskUI.taskRemove_btn.clicked.connect(partial(self.deleteTaskUI, taskUI))
            self.tasksLayout.addLayout(taskUI.getLayout())
            # self.tasksContainer.addLayout(taskUI.getLayout())
            self.allTasksUI.append(taskUI)
        else:
            taskUI = TaskUI(name, status, priority, progress)
            taskUI.taskRemove_btn.clicked.connect(partial(self.deleteTaskUI, taskUI))
            self.tasksLayout.addLayout(taskUI.getLayout())
            # self.tasksContainer.addLayout(taskUI.getLayout())
            self.allTasksUI.append(taskUI)

    def updateTaskUI(self):
        for i in self.allTasksUI:
            print i
    def deleteTaskUI(self, taskUI):
        #print taskUI
        print self.allTasksUI
        taskUI.deleteTask()
        if taskUI in self.allTasksUI:
            self.allTasksUI.remove(taskUI)
            print 'Done'
        print self.allTasksUI

    def saveTodoList(self):
        tasksList = []
        for taskUI in self.allTasksUI:
            print taskUI.taskStatus.currentText()+'-'*10
            tasksList.append(Task(taskUI.taskName.text(), 
                                  taskUI.taskStatus.currentText(),
                                  taskUI.taskPB.value(),
                                  taskUI.taskPriority.currentText()))
        print tasksList
        saver = TaskSaveAndLoader()
        saver.saveTasks(tasksList)

ui = ToDoListUI()
panels.registerWidgetAsPanel('todoList2.ToDoListUI', 'TodoList2', 'fr.victor.ToDoListUI')