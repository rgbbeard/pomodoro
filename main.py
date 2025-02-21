#!/usr/bin/python

from window import *
from thread_maid import ThreadMaid
from time import sleep
from subprocess import Popen, PIPE
from PIL import ImageTk

window_thread = ThreadMaid()
pomodoro_thread = ThreadMaid()

w = None
r = None

label_text = None
button_text = None
timer_text = None
label = None
button = None
timer = None

focus_interval:int = 24 # minutes
pause_interval:int = 4 # minutes
minutes_passed: int = focus_interval
seconds_passed: int = 60 # seconds
paused:bool = False
switched:bool = False


def toggle_bg():
	global r, background, label, button, timer, paused, switched

	if paused or switched:
		fg = "white"
		bg = "green"
	else:
		fg = "black"
		bg = "orange"

	r["bg"] = bg

	label["fg"] = fg
	label["bg"] = bg

	button["fg"] = fg
	button["bg"] = bg

	timer["fg"] = fg
	timer["bg"] = bg


def toggle_pause():
	global paused, label_text, button_text

	paused = not paused

	if label_text is not None and button_text is not None:
		if paused:
			button_text.set("Start")
			label_text.set("Pomodoro paused")
		else:
			button_text.set("Stop")
			label_text.set("Pomodoro running")

	toggle_bg()


def toggle_switched():
	global switched, label_text, button_text

	switched = not switched

	toggle_bg()


def win():
	global w, r, label_text, button_text, timer_text, label, button, timer, minutes_passed, seconds_passed

	w = Window(
		window_name="Pomodoro",
		window_size="200x100"
	)
	r = w.get_root()

	label_text = tkinter.StringVar(r)
	button_text = tkinter.StringVar(r)
	timer_text = tkinter.StringVar(r)

	label_text.set("Pomodoro running")
	button_text.set("Stop")
	timer_text.set(f"{minutes_passed}:{seconds_passed}")

	label = tkinter.Label(r, textvariable=label_text)
	button = tkinter.Button(
		r, 
		textvariable=button_text, 
		command=toggle_pause
	)
	timer = tkinter.Label(r, textvariable=timer_text)

	label.pack()
	button.pack()
	timer.pack()

	toggle_bg()

	w.display()


def pomodoro():
	global r, minutes_passed, seconds_passed, paused, timer_text, switched

	while True:
		if r is not None:
			if not paused:
				seconds_passed -= 1

			m = minutes_passed
			s = seconds_passed

			if minutes_passed < 10:
				m = f"0{minutes_passed}"

			if seconds_passed < 10:
				s = f"0{seconds_passed}"

			timer_text.set(f"{m}:{s}")

			if minutes_passed == 0 and seconds_passed <= 0:
				toggle_bg()
				toggle_switched()

				if not switched:
					minutes_passed = focus_interval
				else:
					minutes_passed = pause_interval	
				seconds_passed = 59

			if seconds_passed <= 0:
				if minutes_passed > 0:
					minutes_passed -= 1
				seconds_passed = 59

			sleep(1) # seconds


window_thread.setup(target=win).run()

"""
	to ensure that all the variables 
	are set before starting the pomodoro
"""
all_set = False

while not all_set:
	for i in [w, r, label_text, button_text, timer_text, label, button, timer]:
		if i is None:
			all_set = False
		else:
			all_set = True

pomodoro_thread.setup(target=pomodoro).run()
