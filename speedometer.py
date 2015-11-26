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

fps = frameRates[cmds.currentUnit(query=True,time=True)]
timeInterval = 1.0 / fps

selectedObjects = cmds.ls(selection=True)
attr = 'speed'
addAttributeToObjects(selectedObjects, attr)

prevPos = []
for obj in selectedObjects:
    prevPos.append(cmds.getAttr(obj + '.translate')[0])

while(currentFrame < endFrame):
    currentFrame += 1
    for k in xrange(0, len(selectedObjects)):
        obj = selectedObjects[k]
        currentPos = cmds.getAttr(obj + '.translate', time=currentFrame)[0]

        speed = getSpeed(prevPos[k], currentPos, timeInterval)

        cmds.setKeyframe(obj, at='speed', v = speed, t = currentFrame)
        prevPos[k] = currentPos

def getSpeed(prevPos, currentPos, dt):
    displacement = math.sqrt(sum((x - y)**2 for x,y in zip(prevPos,currentPos)))
    return displacement / dt

def addAttributeToObjects(objects, attribute):
    for obj in objects:
        if not cmds.attributeQuery(attribute, node=obj, exists=True):
            cmds.addAttr(obj, longName=attribute, defaultValue=0.0, minValue=0.0 )
