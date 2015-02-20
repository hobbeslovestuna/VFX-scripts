'''
    BreakDowner :   a little tool to render the various pass for breakdowns
                    It takes a number of  nodes in input. Plugs some write nodes.
                    Renders out based on the directory structure established in Hobbes
    author      :   Victor
    version     :   0.1
'''
import nuke
import os
import re

import hobbes
reload(hobbes)

filePath = nuke.Root()['name'].value()
h = hobbes.Hobbes(verbose = False)

def BreakDowner(listNodes = nuke.selectedNodes()):

    if listNodes is None or listNodes == []:
        raise TypeError, 'You have not selected any nodes !'

    listWriteNode = []
    for node in listNodes:
        nodeName = node['name'].value()
        wName = 'Write_'+nodeName
        w = nuke.nodes.Write()
        w['name'].setValue(wName)
        w.setInput(0, node)
        listWriteNode.append(w)

    project = h.currentProject(filePath)
    print project
    print h.PROJECTS
    shotNumber = h.currentShot(filePath)#.split('/')[-2]
    print shotNumber
    pathBKD = os.path.join(h.PROJECTS, project, h.SHOTS, h.RENDER, shotNumber)#, 'Breakdown')
    if not os.path.exists(pathBKD):
        try:
            os.mkdir(pathBKD)
        except IOError:
            print 'Error IO'
    pathBKD = os.path.join(pathBKD, 'Breakdown')
    try:
        if not os.path.exists(pathBKD):
            os.mkdir(pathBKD)
        else:
            print 'Already Created'
    except IOError:
        print 'An error occured whil creating the dir'
        return -1

    #We set the correct path for the write nodes
    renderOrder = 1
    for w in listWriteNode:
        fileKnob = os.path.join(pathBKD, w['name'].value())
        fileKnob += '.'+str(nuke.frame())+'.exr'

        w['file_type'].setValue('exr')

        w['file'].setValue(fileKnob)

        #write
        nuke.execute(w['name'].value(), int(nuke.frame()), int(nuke.frame()))