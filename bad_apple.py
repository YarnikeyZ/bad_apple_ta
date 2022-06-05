from PIL import Image
from time import sleep
from datetime import datetime
from subprocess import getoutput as gout
clear = gout("clear")

frames = 6573
y = 50
x = y*2
xy = x*y
sleeptime = 0.0199

input('Press enter and watch...')

starttime = datetime.now()
for num in range(1, frames):
	time = datetime.now()
	file = f"frames/image{num}.jpg"
	img = Image.open(file)
	if x and y != None:
		img = img.resize((x, y), Image.ANTIALIAS)
	zo = img.convert('L').point(lambda x: 0 if x < 128 else 1, '1')
	data = list(zo.getdata())
	start = str(data).replace('[', '').replace(']', '').replace(',', '').replace(' ', '')
	center = '\n'.join([start[i:i+img.size[0]] for i in range(0, len(start), img.size[0])]) if ' ' not in start[:img.size[0]] and len(start) > img.size[0] else start
	print(f'{sleep(sleeptime)}{clear}{str(center).replace("0"," ").replace("1","#")}\n\n"Screen": Resolution/Total/Sum: {x}x{y}/{xy}/{sum(data)} symbols\n\nFrames: Total/Remaining/Now frame(s): {frames}/{frames-num}/{num}\n\nTime: Total/Manual FT/Used FT: {str(datetime.now() - starttime)[3:]}/{sleeptime}/{str(datetime.now() - time)[6:][:5]}\n\a')
