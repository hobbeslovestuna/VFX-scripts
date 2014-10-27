import threading
import time


def doIT():
    n = nuke.selectedNode()
    print '_'*20
    print 'Selected Node on which the calculation will be processed %s' %n['name'].value()
    
    first   = nuke.Root()['first_frame'].value()
    last    = nuke.Root()['last_frame'].value()
    total   = last - first
    currentFrame = nuke.frame()
    
    maxBBoxX = nuke.toNode('FrameBlend1').bbox().x()
    maxBBoxY = nuke.toNode('FrameBlend1').bbox().y()
    maxBBoxR = nuke.toNode('FrameBlend1').bbox().w() + maxBBoxX
    maxBBoxT = nuke.toNode('FrameBlend1').bbox().h() + maxBBoxY
    
    maxBBox = [maxBBoxX, maxBBoxY, maxBBoxR, maxBBoxT]
    print 'Value of the BBox '+str(maxBBox)
    
    task        = nuke.ProgressTask('Getting Frame for max BBox\n value at x,y,r,t on frame %f' % currentFrame)
    progIncr    = 100.0 / total
    result      = []
    for frame in range(first, last):
        if task.isCancelled():
            nuke.executeInMainThread(nuke.message, args=('Calculation aborted'))
            return
        
        
        nuke.frame(frame)
        time.sleep(.1)
        
        if n.bbox().x() == maxBBox[0]:
            print 'x found at frame %f' %frame
            result.append(('x', frame))
        if n.bbox().y() == maxBBox[1]:
            print 'y found at frame %f' %frame
            result.append(('y', frame))
        
        if n.bbox().w() == maxBBox[2]:
            print 'r found at frame %f' %frame
        if n.bbox().h() == maxBBox[3]:
            print 't found at frame %f' %frame
        
        task.setProgress(int(frame * progIncr))
        task.setMessage('Processing frame : '+str(frame))

        nuke.frame(currentFrame)
    return 
threading.Thread(target=doIT).start()
threading.Thread().stop()
print 'DONE'