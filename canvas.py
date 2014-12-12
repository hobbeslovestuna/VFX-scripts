'''
    A simple canvas creator
    TODO : fix the threading and getting of w() and h()
'''
import threading
import time
import nuke

def doIT():
    n = nuke.selectedNode()
    print '_'*20
    print 'Selected Node on which the calculation will be processed %s' %n['name'].value()
    
    first   = nuke.Root()['first_frame'].value()
    last    = nuke.Root()['last_frame'].value()
    total   = last - first
    
    maxBBoxX = nuke.toNode('FrameBlend1').bbox().x()
    maxBBoxY = nuke.toNode('FrameBlend1').bbox().y()
    maxBBoxR = nuke.toNode('FrameBlend1').bbox().w() + maxBBoxX
    maxBBoxT = nuke.toNode('FrameBlend1').bbox().h() + maxBBoxY
    
    maxBBox = [maxBBoxX, maxBBoxY, maxBBoxR, maxBBoxT]
    print 'Value of the BBox '+str(maxBBox)
    
    task        = nuke.ProgressTask('Getting Frame for max BBox\n value at x,y,r,t')
    progIncr    = 100.0 / total
    result      = []
    for frame in xrange(int(first), int(last)):
        
        frame = float(frame)

        if task.isCancelled():
            nuke.executeInMainThread(nuke.message, args=('Calculation aborted'))
            return
        
        
        nuke.frame(frame)
        time.sleep(.1)
        
        # if n.bbox().x() == maxBBox[0]:
        #     print 'x found at frame %f' %frame
        #     result.append(('x', frame))
        # if n.bbox().y() == maxBBox[1]:
        #     print 'y found at frame %f' %frame
        #     result.append(('y', frame))
        print frame, n.bbox().w()-maxBBox[0], maxBBox[2]
        if n.bbox().w() == maxBBox[2]:
            print 'r found at frame %f' %frame
        if n.bbox().h() == maxBBox[3]:
            print 't found at frame %f' %frame
        
        task.setProgress(int(frame * progIncr))
        task.setMessage('Processing frame : '+str(frame))

    return 
threading.Thread(target=doIT).start()
#threading.Thread().stop()
print 'DONE'