import maya.cmds as cmds
import math

def getSpeed(prevPos, currentPos, dt):
    displacement = math.sqrt(sum((x - y)**2 for x,y in zip(prevPos,currentPos)))
    return displacement / dt

def addAttributeToObjects(objects, attr):
    for obj in objects:
        if cmds.attributeQuery(attr, node=obj, exists=True):
            cmds.deleteAttr(obj, attribute=attr)
        cmds.addAttr(obj, longName=attr, defaultValue=0.0, minValue=0.0)

def findSpeeds(arg):
    frameRates = {
        'game': 15,
        'film': 24,
        'pal': 25,
        'ntsc': 30,
        'show': 48,
        'palf': 50,
        'ntscf': 60
    }

    first_user_frame = cmds.intField(window_UI['first_frame'], query=True, value=True)
    last_user_frame = cmds.intField(window_UI['last_frame'], query=True, value=True)

    start_frame = cmds.playbackOptions(query=True, minTime=True)
    end_frame = cmds.playbackOptions(query=True, maxTime=True)

    if first_user_frame < start_frame or last_user_frame > end_frame:
        return

    current_frame = first_user_frame

    fps = frameRates[cmds.currentUnit(query=True,time=True)]
    timeInterval = 1.0 / fps

    selectedObjects = cmds.ls(selection=True)
    attr = 'speed'
    addAttributeToObjects(selectedObjects, attr)

    prevPos = []
    for obj in selectedObjects:
        prevPos.append(cmds.getAttr(obj + '.translate')[0])

    while(current_frame < last_user_frame):
        current_frame += 1
        for k in xrange(0, len(selectedObjects)):
            obj = selectedObjects[k]
            currentPos = cmds.getAttr(obj + '.translate', time=current_frame)[0]

            speed = getSpeed(prevPos[k], currentPos, timeInterval)

            cmds.setKeyframe(obj, at='speed', v = speed, t = current_frame)
            prevPos[k] = currentPos

window_id = 'speedometer_UI_v1'
if cmds.window(window_id, exists=True):
    cmds.deleteUI(window_id)

def checkIfUpdateValid(arg):
    frame1 = cmds.intField(window_UI['first_frame'], query=True, value=True)
    frame2 = cmds.intField(window_UI['last_frame'], query=True, value=True)
    cmds.disable( window_UI['button'], v= frame1 >= frame2 )

def createWindow(id):
  win = cmds.window(id, title = 'Speedometer')
  cl1 = cmds.columnLayout(adjustableColumn = True, rowSpacing = 10)
  rl1 = cmds.rowColumnLayout(parent = cl1, numberOfColumns = 2)
  tx1 = cmds.text( label = 'Start Frame')
  tx2 = cmds.text( label = 'End Frame')
  first_frame = cmds.intField( value = 1, changeCommand = checkIfUpdateValid )
  last_frame = cmds.intField( value = 2, changeCommand = checkIfUpdateValid )
  my_button = cmds.button(parent = cl1, label = "Find Speed", command=findSpeeds )
  cmds.showWindow(win)
  window_UI = {'win':win,
               'first_frame':first_frame,
               'last_frame': last_frame,
               'button': my_button}
  return window_UI

window_UI = createWindow(window_id)