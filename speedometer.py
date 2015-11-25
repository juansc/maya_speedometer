import maya.cmds as cmds
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
obj = cmds.ls(selection=True)[0]

objPos = cmds.getAttr(obj + '.translate')[0]
previousX = objPos[0]
previousY = objPos[1]
previousZ = objPos[2]

currentFrame = startFrame

cmds.window( width =150 )
cmds.showWindow()

while(currentFrame < endFrame):
    currentFrame += 1

    objPos = cmds.getAttr(obj + '.translate', time=currentFrame)[0]
    currentX, currentY, currentZ = objPos[0], objPos[1], objPos[2]

    dx = (currentX - previousX) ** 2
    dy = (currentY - previousY) ** 2
    dz = (currentZ - previousZ) ** 2
    displacement = math.sqrt(dx + dy + dz)
    speed = displacement / timeInterval

    cmds.setKeyframe(obj, at='speed', v = speed, t = currentFrame)

    previousX, previousY, previousZ  = currentX, currentY, currentZ



# #
# import maya.cmds as cmds
# startFrame = cmds.playbackOptions(query=True, minTime=True)
# endFrame = cmds.playbackOptions(query=True, maxTime=True)
# endFrame = 300
# obj = cmds.ls(selection=True)

# objPos = cmds.getAttr(obj[0] + '.translate')[0]

# cmds.setKeyframe(obj, at='translateX', v = objPos[0], t = startFrame)
# cmds.setKeyframe(obj, at='translateY', v = objPos[1], t = startFrame)
# cmds.setKeyframe(obj, at='translateZ', v = objPos[2], t = startFrame)
# cmds.setKeyframe(obj, at='rotateX', v = 0.0, t = startFrame)
# cmds.setKeyframe(obj, at='rotateY', v = 0.0, t = startFrame)
# cmds.setKeyframe(obj, at='rotateZ', v = 0.0, t = startFrame)

# cmds.setKeyframe(obj, at='translateX', v = 0.0, t = endFrame)
# cmds.setKeyframe(obj, at='translateY', v = 0.0, t = endFrame)
# cmds.setKeyframe(obj, at='translateZ', v = 0.0, t = endFrame)
# cmds.setKeyframe(obj, at='rotateX', v = 720.0, t = endFrame)
# cmds.setKeyframe(obj, at='rotateY', v = 720.0, t = endFrame)
# cmds.setKeyframe(obj, at='rotateZ', v = 720.0, t = endFrame)
# #