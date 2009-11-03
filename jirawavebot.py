from waveapi import events
#from waveapi import model
from waveapi import robot
import re

JIRAMATCH = re.compile("(\s|^)(FEAT|INF|DOCUS|INT)(-\d+)(\D)", re.I)
JIRASUB   = " http://jira.texturallc.net/browse/\\2\\3\\4"

def OnParticipantsChanged(properties, context):
  """Invoked when any participants have been added/removed."""
  added = properties['participantsAdded']
  for party in added:
    Notify(context, party)

def OnBlipSubmit(properties, context):
  blip = context.GetBlipById(properties['blipId'])
  contents = blip.GetDocument().GetText()
  newcons = contents + 'http://www.texturacorp.com'
  hasRef = linkCases(contents)
  if hasRef:
    blip.GetDocument().SetText(hasRef)
  #root_wavelet = context.GetRootWavelet()
  #root_wavelet.CreateBlip().GetDocument().SetText(newcons)

def OnDocumentChanged(properties, context):
  blip = context.GetBlipById(properties['blipId'])
  contents = blip.GetDocument().GetText()
  newcons = contents + 'http://www.texturacorp.com'
  hasRef = linkCases(contents)
  if hasRef:
    blip.GetDocument().SetText(hasRef)
  #root_wavelet = context.GetRootWavelet()
  #root_wavelet.CreateBlip().GetDocument().SetText(newcons)

def echoBlip(new, blip, ctx):
  new.SetText('You said: "' + blip.GetText() + '"' + str(ctx))


def linkCases(s):
  if re.search(JIRAMATCH, s):
    ret = re.sub(JIRAMATCH, JIRASUB, s)
  else:
    ret = None
  return ret

def OnRobotAdded(properties, context):
  """Invoked when the robot has been added."""
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("I'm alive!")

def Notify(context, party):
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("Hi " + party + "!")

if __name__ == '__main__':
  myRobot = robot.Robot('jirawavebot',
      image_url='http://jirawavebot.appspot.com/assets/python.jpg',
      version='1',
      profile_url='http://jirawavebot.appspot.com/')
  myRobot.RegisterHandler(events.WAVELET_PARTICIPANTS_CHANGED, OnParticipantsChanged)
  myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
  myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmit)
  myRobot.RegisterHandler(events.DOCUMENT_CHANGED, OnDocumentChanged)
  myRobot.Run()
