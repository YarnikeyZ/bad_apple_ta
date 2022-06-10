from PIL import Image
from time import sleep
from datetime import datetime
from subprocess import getoutput as gout
from sys import argv
from os import listdir as ld


clear = gout("clear")


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
		print(progress(count, num, inper, ("█", " "))[1], end="")
		inper = progress(count, num, inper, ("█", " "))[0]
		frames.append(f'{pic}\n\n"Screen": Resolution/Total: {x}x{y}/{xy} symbols\n\nFrames: Total/Remaining/Now frame(s): {count}/{count-num}/{num}')
	return frames


def display(frames: list, frame_time: float):
	input("Display?...")
	time_st = datetime.now()
	for frame in frames:
		time_frame = datetime.now()
		print(f"{sleep(frame_time)}{clear}\n\n\n\n{frame}\n\nTime Total/Manual FT/Used FT: {datetime.now() - time_st}/{frame_time}/", end="")
		print(datetime.now() - time_frame)


def write_frames(frames: list):
	inper = 0
	count = len(frames)
	for img_frame, num in zip(frames, range(1, count)):
		with open(f"txt_frames/frame{num}.txt", 'w', encoding="utf-8") as txt_frame:
			txt_frame.write(img_frame)
		print(progress(count, num, inper, ("█", " "))[1], end="")
		inper = progress(count, num, inper, ("█", " "))[0]
	return


def read_frames():
	frames = []
	inper = 0
	count = len(ld("txt_frames"))
	for num in range(1, count):
		with open(f"txt_frames/frame{num}.txt", "r", encoding="utf-8") as frame:
			frames.append(frame.read())
		print(progress(count, num, inper, ("█", " "))[1], end="")
		inper = progress(count, num, inper, ("█", " "))[0]
	return frames


def main(action: str, y: int, frame_time: float, path: str):
	try:
		frames = []
		path = f"img_frames_{path}"
		count = len(ld(path))
		if action == "WR-REND" or action == "WR":
			frames = render(path, y)
			write_frames(frames)
			return
		elif action == "READ-REND" or action == "READ":
			frames = read_frames()
			display(frames, frame_time)
			return
		else:
			frames = render(path, y)
			display(frames, frame_time)
			return
	except KeyboardInterrupt:
		print("\n[ok]\n")
		exit()


if __name__ == "__main__":
	try:
		try:
			##Argv handling
			main(
				argv[1],
				int(argv[2]),
				float(argv[3]),
				argv[4]
			)
		except IndexError:
			##No argv handling
			main(
				input("Chose action (WR-REND or WR to write render, READ-REND or READ to read render, REND render): ").upper(),
				int(input("Y: ")),
				float(input("Frame time: ")),
				input("Path to frames: img_frames_")
			)
	except KeyboardInterrupt:
		print("\n\nExiting...")
		exit()
