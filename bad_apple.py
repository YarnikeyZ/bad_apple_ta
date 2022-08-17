from PIL import Image
from time import sleep as sl
from datetime import datetime, timedelta
from subprocess import getoutput as gout
from sys import argv
from os import listdir as ls

clear = gout("clear")
script_dir = __file__[:__file__.rfind('/')-len(__file__)+1]

def progress(all: int, part: int, inper: int, symbs: tuple):
	per = round((part/all)*100)
	if inper != per:
		return (per, f"\033[1A({''.ljust(per, symbs[0])}{''.ljust(100-per, symbs[1])}) [{str(per).rjust(3, ' ')}]%\n")
	else:
		return (per, "")

def render(path: str, y: int):
	frames = []
	x = y*2
	xy = x*y
	inper = 0
	sscale = ['.', "'", ',', ':', '^', '"', ';', '*', '!', '²', '¤', '/', 'r', '(', '?', '+', '?', 'c', 'L', 'ª', '7', 't', '1', 'f', 'J', 'C', 'Ý', 'y', '¢', 'z', 'F', '3', '±', '%', '2', 'k', 'ñ', '5', 'A', 'Z', 'X', 'G', '$', 'À', '0', 'Ã', 'm', '&', 'Q', '8', '#', 'R', 'Ô', 'ß', 'Ê', 'N', 'B', 'å', 'M', 'Æ', 'Ø', '@', '¶']
	cscale  = [0, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 15]
	count = len(ls(path))
	for num in range(1, count):
		img = Image.open(f"{path}/frame{num}.jpg").convert('L')
		img = img.resize((x, y), Image.Resampling.LANCZOS)
		obj = img.load()
		pic = ''
		for y_pix in range(0, img.size[1]):
			for x_pix in range(0, img.size[0]):
				cbright = obj[x_pix, y_pix]//9
				sbright = obj[x_pix, y_pix]//4
				if sbright == 0:
					sbright =+ 1
				if cbright > 25:
					cbright = 25
				elif cbright < 1:
					cbright = 0
				pic += f'\033[38;5;{cscale[cbright]}m{sscale[sbright-1]}\033[0;0m'
			pic += '\n'
		prog = progress(count, num, inper, ("█", " "))
		print(prog[1], end="")
		inper = prog[0]
		frames.append(f'{pic}\n\n"Screen": Resolution/Total: {x}x{y}/{xy} symbols\nFrames: Total/Remaining/Now frame(s): {count}/{count-num}/{num}         ')
	return frames

def display(frames: list, fps: int):
	input("Display?...")
	print(clear)
	remaining = 0
	overflow = 0
	display_start = datetime.now()
	for frame in frames:
		print(f"\033[1007A", end="")
		frame_time = datetime.now()
		print(frame)
		manual_frame_time = 1/fps - (datetime.now() - frame_time).microseconds/1000000-remaining
		if manual_frame_time > 0:
			sl(manual_frame_time)
			remaining = 0
		else:
			overflow += 1
			remaining = manual_frame_time*-1
		print(f'Time Total/FPS/Preset FT/Manual FT/Used FT/Overflowed: {datetime.now() - display_start}/{fps}/{1/fps}/{manual_frame_time}/{datetime.now() - frame_time}/{overflow}          ')

def write_frames(frames: list):
	inper = 0
	count = len(frames)
	for img_frame, num in zip(frames, range(1, count)):
		with open(f"{script_dir}txt_frames/frame{num}.txt", 'w', encoding="utf-8") as txt_frame:
			txt_frame.write(img_frame)
		prog = progress(count, num, inper, ("█", " "))
		print(prog[1], end="")
		inper = prog[0]
	return

def read_frames():
	frames = []
	inper = 0
	count = len(ls(f"{script_dir}txt_frames"))
	for num in range(1, count):
		with open(f"{script_dir}txt_frames/frame{num}.txt", "r", encoding="utf-8") as frame:
			frames.append(frame.read())
		prog = progress(count, num, inper, ("█", " "))
		print(prog[1], end="")
		inper = prog[0]
	return frames

def main():
	try:
		try:
			if argv[1].upper() in ["WR-REND", "WR"]:
				write_frames(render(f"{script_dir}img_frames_{argv[2]}", int(argv[3])))

			elif argv[1].upper() in ["READ-REND", "READ"]:
				frames = read_frames()
				display(frames, int(argv[2]))
			
			elif argv[1].upper() == "REND":
				display(render(f"{script_dir}img_frames_{argv[2]}", int(argv[4])), int(argv[3]))
			
			else:
				print(argv)
			
		except IndexError:
			action = input("Chose action (WR-REND or WR to write render, READ-REND or READ to read render, REND render): ").upper()
			if action in ["WR-REND", "WR"]:
				write_frames(render(f"{script_dir}img_frames_{input('Path to frames: img_frames_')}", int(input("Y: "))))
			
			elif action in ["READ-REND", "READ"]:
				frames = read_frames()
				display(frames, int(input("FPS: ")))
			
			elif action == "REND":
				display(render(f"{script_dir}img_frames_{input('Path to frames: img_frames_')}", int(input("Y: "))), int(input("FPS: ")))
			
			else:
				print(argv)
	
	except KeyboardInterrupt:
		print("\n[ok]\n")
		exit()

if __name__ == "__main__":
	main()
