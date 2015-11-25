import maya.cmds as cmds
import math

def addAttributeToObjects(objects, attribute):
    for obj in objects:
        if not cmds.attributeQuery(attribute, node=obj, exists=True):
            cmds.addAttr(obj, longName=attribute, defaultValue=0.0, minValue=0.0 )

frameRates = {
    'game': 15,
    'film': 24,
    'pal': 25,
    'ntsc': 30,
    'show': 48,
    'palf': 50,
    'ntscf': 60
}

startFrame = cmds.playbackOptions(query=True, minTime=True)
endFrame = cmds.playbackOptions(query=True, maxTime=True)
framesPerSecond = frameRates[cmds.currentUnit(query=True,time=True)]
timeInterval = 1.0 / framesPerSecond

objects = cmds.ls(selection=True)[0]
attr = 'speed'

addAttributeToObjects([objects], attr)

objPos = cmds.getAttr(obj + '.translate')[0]

previousX, previousY, previousZ = objPos[:3]

currentFrame = startFrame

print "Current frame is %s" % startFrame
print "Beginning Frame is %s" % endFrame

while(currentFrame < endFrame):
    currentFrame += 1
    objPos = cmds.getAttr(obj + '.translate', time=currentFrame)[0]
    currentX, currentY, currentZ = objPos[:3]

    dx = (currentX - previousX) ** 2
    dy = (currentY - previousY) ** 2
    dz = (currentZ - previousZ) ** 2
    displacement = math.sqrt(dx + dy + dz)
    speed = displacement / timeInterval

    cmds.setKeyframe(obj, at='speed', v = speed, t = currentFrame)
    print speed
    print "X: %s Y: %s Z: %s" % (currentX, currentY, currentZ)
    previousX, previousY, previousZ  = currentX, currentY, currentZ
