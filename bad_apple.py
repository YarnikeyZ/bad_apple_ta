from PIL import Image
from time import sleep as sl
from datetime import datetime
from subprocess import getoutput as gout
from sys import argv
from os import listdir as ld


clear = gout("clear")


def mv_p(way: str, length: int):
	mv = "\u001b["
	way = way.upper()
	if way == "U" or way == "A":
		print(f"{mv}{length}A", end="")
	elif way == "D" or way == "B":
		print(f"{mv}{length}B", end="")
	elif way == "R" or way == "C":
		print(f"{mv}{length}C", end="")
	elif way == "L" or way == "D":
		print(f"{mv}{length}D", end="")


def progress(all: int, part: int, inper: int, symbs: tuple):
	per = round((part/all)*100)
	if inper != per:
		return (per, f"({''.ljust(per, symbs[0])}{''.ljust(100-per, symbs[1])}) [{str(per).rjust(3, ' ')}]%\n")
	else:
		return (per, "")


def render(path: str, y: int):
	frames = []
	x = y*2
	xy = x*y
	inper = 0
	sscale = ['.', "'", ',', ':', '^', '"', ';', '*', '!', '²', '¤', '/', 'r', '(', '?', '+', '?', 'c', 'L', 'ª', '7', 't', '1', 'f', 'J', 'C', 'Ý', 'y', '¢', 'z', 'F', '3', '±', '%', '2', 'k', 'ñ', '5', 'A', 'Z', 'X', 'G', '$', 'À', '0', 'Ã', 'm', '&', 'Q', '8', '#', 'R', 'Ô', 'ß', 'Ê', 'N', 'B', 'å', 'M', 'Æ', 'Ø', '@', '¶']
	cscale  = [0, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 15]
	count = len(ld(path))
	for num in range(1, count):
		img = Image.open(f"{path}/frame{num}.jpg").convert('L')
		img = img.resize((x, y), Image.Resampling.LANCZOS)
		obj = img.load()
		pic = ''
		for y_pix in range(0, img.size[1]):
			line = ''
			for x_pix in range(0, img.size[0]):
				cbright = obj[x_pix, y_pix]//9
				sbright = obj[x_pix, y_pix]//4
				if sbright == 0:
					sbright =+ 1
				if cbright > 25:
					cbright = 25
				elif cbright < 1:
					cbright = 0
				line += f'\033[38;5;{cscale[cbright]}m{sscale[sbright-1]}\033[0;0m'
			pic += f'{line}\n'
		prog = progress(count, num, inper, ("█", " "))
		print(prog[1], end="")
		inper = prog[0]
		frames.append(f'{pic}\n\n"Screen": Resolution/Total: {x}x{y}/{xy} symbols\n\nFrames: Total/Remaining/Now frame(s): {count}/{count-num}/{num}')
	return frames


def display(frames: list, frame_time: float, y: int):
	input("Display?...")
	print(clear)
	time_st = datetime.now()
	for frame in frames:
		mv_p('U', y+3)
		time_frame = datetime.now()
		sl(frame_time)
		for line in frame.split("\n"):
			print(line)
		print(f'\nTime Total/Manual FT/Used FT: {datetime.now() - time_st}/{frame_time}/{datetime.now() - time_frame}')


def write_frames(frames: list):
	inper = 0
	count = len(frames)
	for img_frame, num in zip(frames, range(1, count)):
		with open(f"txt_frames/frame{num}.txt", 'w', encoding="utf-8") as txt_frame:
			txt_frame.write(img_frame)
		prog = progress(count, num, inper, ("█", " "))
		print(prog[1], end="")
		inper = prog[0]
	return


def read_frames():
	frames = []
	inper = 0
	count = len(ld("txt_frames"))
	for num in range(1, count):
		with open(f"txt_frames/frame{num}.txt", "r", encoding="utf-8") as frame:
			frames.append(frame.read())
		prog = progress(count, num, inper, ("█", " "))
		print(prog[1], end="")
		inper = prog[0]
	return frames


def main():
	try:
		action = input("Chose action (WR-REND or WR to write render, READ-REND or READ to read render, REND render): ").upper()
		if action == "WR-REND" or action == "WR":
			y = int(input("Y: "))
			frame_time = 0
			path = f"img_frames_{input('Path to frames: img_frames_')}"
			frames = render(path, y)
			write_frames(frames)
			return
		elif action == "READ-REND" or action == "READ":
			frame_time = float(input("Frame time: "))
			path = ""
			frames = read_frames()
			y = len(frames[0].split("\n"))
			display(frames, frame_time, y+4)
			return
		else:
			y = int(input("Y: "))
			frame_time = float(input("Frame time: "))
			path = f"img_frames_{input('Path to frames: img_frames_')}"
			frames = render(path, y)
			display(frames, frame_time , y+4)
			return
	except KeyboardInterrupt:
		print("\n[ok]\n")
		exit()


if __name__ == "__main__":
	main()
