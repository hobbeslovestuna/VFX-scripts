import nuke
import nukescripts
import re

def getDatas():
    '''
        Retrieves the data from the cameraTracker node to get the right placement in 3D for the projections card
        Returns :
            listData -> A list containing dictionnaries for each userTrack with the xyz position
    '''
    try:
        node = nuke.selectedNode()
    except ValueError:
        node = None
    if node == None:
        nuke.message('You must select a node ! A camera tracker node is what you need')
        return -1
    elif node.Class() != 'CameraTracker':
        nuke.message('You must select a CameraTracker Node to get datas !')
        return -1
    else:
        
        pointsData = node.knob('userTracks').toScript()
        pointsDataFile = open('/home/victor/data.log', 'w')
        pointsDataFile.write(pointsData)
        pointsDataFile.close()

        listData = []
        pointsDataFile = open('/home/victor/data.log', 'r')
        for line in pointsDataFile.readlines():
            if re.search("user [0-9]{1,}", line):
                userTrack = re.search("user [0-9]{1,}", line).group()
                line = line.split('{curve} {curve} {curve} {curve}')[-1].split()
                line = [float(line[1]), float(line[2]), float(line[3])]

                userTrackDict = dict(zip(['userTrackName', 'xyz'], [userTrack, line]))
                listData.append(userTrackDict)

        return listData

def createProjectionSetup(listData):
    '''
        Creates the projection setup with a project3D node per card and a dot connected 
        Returns : None
    '''

    try:
        cameraTrackerNode = nuke.selectedNode()
    except ValueError:
        print 'You must select a camera Tracker node !'
        return -1
    cameraTrackerPosition = [cameraTrackerNode.xpos(), cameraTrackerNode.ypos()]
    
    numOfCards = len(listData)
    readNode = nuke.selectedNode().input(0)['name'].value()
 
    for userTrack in listData:
        #print i
        print userTrack['xyz']
        print '_'*30

        projection(userTrack)

def projection(userTrackData, offset = 0):

    try:
        cameraTrackerNode = nuke.selectedNode()
    except ValueError:
        print 'You must select a camera Tracker node !'
        return -1
    cameraTrackerPosition = [cameraTrackerNode.xpos(), cameraTrackerNode.ypos()]
    
    dotPlate = nuke.createNode("Dot")
    dotPlate['label'].setValue("PLATE")

    dotCamera = nuke.createNode("Dot")
    dotCamera['label'].setValue("CAMERA")

    dotPlate.setXpos(cameraTrackerPosition[0] - 100)
    dotPlate.setYpos(cameraTrackerPosition[1] + 3)

    dotCamera.setXpos(cameraTrackerPosition[0] - 150)
    dotCamera.setYpos(cameraTrackerPosition[1] - 30)

    dotPlate.setInput(0, cameraTrackerNode)
    dotCamera.setInput(0, nuke.toNode('Camera1'))

    #--Project3D
    projection3DNode = nuke.createNode('Project3D')
    projection3DNode.setYpos(dotPlate.ypos()+130)
    projection3DNode.setXpos(dotPlate.xpos()-34)

    dotCam2 = nuke.createNode("Dot")
    dotCam2.setXpos(dotCamera.xpos())
    dotCam2.setYpos(projection3DNode.ypos())
    dotCam2.setInput(0, dotCamera)

    projection3DNode.setInput(0, dotPlate)
    projection3DNode.setInput(1, dotCam2)

    #--card
    card = nuke.createNode("Card2")
    card['translate'].setValue(userTrackData['xyz'])
    card.setInput(0, projection3DNode)
    card.setXpos(projection3DNode.xpos())
    card.setYpos(projection3DNode.ypos() + 30)
    
    #--scanlineRender
    scanline = nuke.createNode("ScanlineRender")
    scanline['projection_mode'].setValue('uv')
    scanline.setXYpos(card.xpos(), card.ypos() + 40)

    #--Reformat
    reformat = nuke.createNode("Reformat")
    reformat.setXYpos(scanline.xpos() - 131 , scanline.ypos() - 6)
    reformat['format'].setValue('square_2K')
    reformat.setInput(0, None)

    scanline.setInput(0, reformat)
    scanline.setInput(1, card)

def proj2(userTrackDatas):

    try:
        cameraTrackerNode = nuke.selectedNode()
    except ValueError:
        print 'You must select a camera Tracker node !'
        return -1
    cameraTrackerPosition = [cameraTrackerNode.xpos(), cameraTrackerNode.ypos()]
    
    lastDotPlate = None
    lastDotCam = None
    
    for userTrackData in userTrackDatas:#range(1, numOcc+1):
        if userTrackDatas.index(userTrackData) == 0:
            dotPlate = nuke.createNode("Dot")
            dotPlate['label'].setValue("PLATE")

            dotCamera = nuke.createNode("Dot")
            dotCamera['label'].setValue("CAMERA")

            dotPlate.setXpos(cameraTrackerPosition[0] - 100)
            dotPlate.setYpos(cameraTrackerPosition[1] + 3)

            dotCamera.setXpos(cameraTrackerPosition[0] - 150)
            dotCamera.setYpos(cameraTrackerPosition[1] - 30)

            dotPlate.setInput(0, cameraTrackerNode)
            dotCamera.setInput(0, nuke.toNode('Camera1'))

            lastDotPlate = dotPlate
            lastDotCam = dotCamera

             #--Project3D
            projection3DNode = nuke.createNode('Project3D')
            projection3DNode.setYpos(dotPlate.ypos()+130)
            projection3DNode.setXpos(dotPlate.xpos()-34)

            dotCam2 = nuke.createNode("Dot")
            dotCam2.setXpos(dotCamera.xpos())
            dotCam2.setYpos(projection3DNode.ypos())
            dotCam2.setInput(0, dotCamera)

            projection3DNode.setInput(0, dotPlate)
            projection3DNode.setInput(1, dotCam2)

            #--card
            card = nuke.createNode("Card2")
            card['translate'].setValue(userTrackData['xyz'])
            card['uniform_scale'].setValue(0.06)
            card.setInput(0, projection3DNode)
            card.setXpos(projection3DNode.xpos())
            card.setYpos(projection3DNode.ypos() + 30)
            
            #--scanlineRender
            scanline = nuke.createNode("ScanlineRender")
            scanline['projection_mode'].setValue('uv')
            scanline.setXYpos(card.xpos(), card.ypos() + 40)

            #--Reformat
            reformatNode = nuke.createNode("Reformat")
            reformatNode.setXYpos(scanline.xpos() - 131 , scanline.ypos() - 6)
            reformatNode['format'].setValue('square_2K')
            reformatNode.setInput(0, None)

            scanline.setInput(0, None)
            scanline.setInput(1, card)
            scanline.setInput(2, None)
            scanline.setInput(0, reformatNode)

        else:
            lastDotPlate_Position = [lastDotPlate.xpos(), lastDotPlate.ypos()]
            lastDotCam_Position = [lastDotCam.xpos(), lastDotCam.ypos()]
            dotPlate = nuke.createNode("Dot")
            dotPlate['label'].setValue("PLATE")

            dotCamera = nuke.createNode("Dot")
            dotCamera['label'].setValue("CAMERA")

            dotPlate.setXpos(lastDotPlate_Position[0] - 300)
            dotPlate.setYpos(lastDotPlate_Position[1])

            dotCamera.setXpos(lastDotCam_Position[0] - 300)
            dotCamera.setYpos(lastDotCam_Position[1])

            dotPlate.setInput(0, lastDotPlate)
            dotCamera.setInput(0, lastDotCam)

             #--Project3D
            projection3DNode = nuke.createNode('Project3D')
            projection3DNode.setYpos(dotPlate.ypos()+130)
            projection3DNode.setXpos(dotPlate.xpos()-34)

            dotCam2 = nuke.createNode("Dot")
            dotCam2.setXpos(dotCamera.xpos())
            dotCam2.setYpos(projection3DNode.ypos())
            dotCam2.setInput(0, dotCamera)

            projection3DNode.setInput(0, dotPlate)
            projection3DNode.setInput(1, dotCam2)

            #--card
            card = nuke.createNode("Card2")
            card['translate'].setValue(userTrackData['xyz'])
            card['uniform_scale'].setValue(0.06)
            card.setInput(0, projection3DNode)
            card.setXpos(projection3DNode.xpos())
            card.setYpos(projection3DNode.ypos() + 30)
            
            #--scanlineRender
            scanline = nuke.createNode("ScanlineRender")
            scanline['projection_mode'].setValue('uv')
            scanline.setXYpos(card.xpos(), card.ypos() + 40)

            #--Reformat
            reformat = nuke.createNode("Reformat")
            reformat.setXYpos(scanline.xpos() - 131 , scanline.ypos() - 6)
            reformat['format'].setValue('square_2K')
            reformat.setInput(0, None)

            scanline.setInput(0, None)
            scanline.setInput(1, card)
            scanline.setInput(2, None)
            scanline.setInput(0, reformat)
            
            lastDotPlate = dotPlate
            lastDotCam = dotCamera
