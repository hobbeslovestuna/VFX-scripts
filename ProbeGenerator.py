#----------------------
#   ProbeGenerator : A tool to generate HDRI images to light in Maya
#   Author  : Victor
#   version : 0.1
#   TODO    : A func to set up the template
#             A func to check and create the formats based on the ratio of the hdr
#             A Panel to adjust the attributes
# print nuke.Root().format().width()
# print nuke.selectedNode()['format'].value().height()

# w = 2809*0.1844
# h = 1873 * 0.024

# crop = nuke.selectedNode()
# crop['box'].setValue((w,h, 2809.0-w, 1873.0 ))
#----------------------
import nuke
import os

#Get the current selected nodes and check if they fit 
hdrs = nuke.selectedNodes()

#Start by setting in place the nodes
if len(hdrs)  < 2:
    print 'Need to select more than 2 Read Nodes'
else:
    positionsY = [float(node.ypos()) for node in hdrs]
    positionsX = [float(node.xpos()) for node in hdrs]
    avgY = sum(positionsY) / len(positionsY)
    avgX = sum(positionsX) /len(positionsX)

    #Order the Read nodes by file name----------------


    for hdrNode in hdrs:
        if hdrNode['file'].value().split('.')[-1] not in ('hdr', 'HDR', 'Hdr'):
            nuke.critical('Wrong file format for %s' %hdrNode)
        else:
            print '_'*50
            print 'Node being processed %s' %hdrNode['name'].value()
            avgX += hdrNode.width() / 10
            hdrNode.setYpos(avgY)
            hdrNode.setXpos(avgX)
            
            #Grade nodes creation
            gradeNode = nuke.createNode('Grade')
            gradeNode.setInput(0, hdrNode)
            gradeNode.setYpos(gradeNode.ypos()+10)
            print '\tGrade node created : %s' %gradeNode

            #Crop nodes creation
            cropNode = nuke.createNode('Crop')
            cropNode['reformat'].setValue(True)
            cropNode.setInput(0, gradeNode)

            #Shuffle nodes creation
            shuffleNode = nuke.createNode('Shuffle')
            #TODO Add an alpha
            shuffleNode.setInput(0, cropNode)

            #Create a Format with the aspect Ratio 2:1 to unwrap the lat long map
            #only once
            #nuke.addFormat(" ")
            
            #Spherical Transforms nodes creation
            sphericalNode = nuke.createNode('SphericalTransform')
            sphericalNode.setInput(0, shuffleNode)
            sphericalNode['input'].setValue('Fisheye')
            sphericalNode['rot_order'].SetValue('ZYX')
            #TODO Set output Format. See how to check if a format exists, how to list them


            #Done