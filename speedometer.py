startFrame = cmds.playbackOptions(query=True, minTime=True)
endFrame = cmds.playbackOptions(query=True, maxTime=True)
framesPerSecond = cmds.playbackOptions(query=True, framesPerSecond=True)
timeInterval = 1.0 / framesPerSecond
obj = cmds.ls(selection=True)

objPos = cmds.getAttr(obj[0] + '.translate')[0]
previousX = objPos[0]
previousY = objPos[1]
previousZ = objPos[2]

currentFrame = startFrame

cmds.window( width =150 )
cmds.showWindow()

while(currentFrame < endFrame):
    currentFrame += 1

    currentX, currentY, currentZ = objPos[0], objPos[1], objPos[2]

    dx = (currentX - previousX) ** 2
    dy = (currentY - previousY) ** 2
    dz = (currentZ - previousZ) ** 2
    displacement = math.sqrt(dx + dy + dz)
    speed = displacement / timeInterval



    previousX, previousY, previousZ  = currentX, currentY, currentZ

