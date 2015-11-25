import maya.cmds as cmds
import math

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
currentFrame = startFrame

framesPerSecond = frameRates[cmds.currentUnit(query=True,time=True)]
timeInterval = 1.0 / framesPerSecond

objects = cmds.ls(selection=True)[0]
attr = 'speed'

addAttributeToObjects([objects], attr)

objPos = cmds.getAttr(obj + '.translate')[0]

prevPos = objPos[:3]

while(currentFrame < endFrame):
    currentFrame += 1

    objPos = cmds.getAttr(obj + '.translate', time=currentFrame)[0]
    currentPos = objPos[:3]

    speed = getSpeed(prevPos, currentPos, timeInterval)

    cmds.setKeyframe(obj, at='speed', v = speed, t = currentFrame)
    prevPos = currentPos

    currentX, currentY, currentZ = currentPos
    print "X: %s Y: %s Z: %s" % (currentX, currentY, currentZ)

def getSpeed(prevPos, currentPos, dt):
    displacement = math.sqrt(sum((x - y)**2 for x,y in zip(prevPos,currentPos)))
    return displacement / dt

def addAttributeToObjects(objects, attribute):
    for obj in objects:
        if not cmds.attributeQuery(attribute, node=obj, exists=True):
            cmds.addAttr(obj, longName=attribute, defaultValue=0.0, minValue=0.0 )
