'''_________________
   vTodoList   : a simple TodoList widget for nuke to help organize your work
   author      : Victor Fleury
   version     : 0.1
'''
import os
from xml.etree import ElementTree as Etree
import nuke

class Task(object):

    def __init__(self):
        '''
            Init of the Task class.
            3 params :
                -_name
                -_priority
                -_amount done
        '''
        self._name      = ''
        self._priority  = 0
        self._amount    = 0

    def create(self, name, prio):
        '''
            Create a task and stores it in the XML
        '''
