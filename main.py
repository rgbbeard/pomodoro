#!/usr/bin/python

from window import *
from thread_maid import ThreadMaid
from time import sleep
from subprocess import Popen, PIPE

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


def toggle_bg():
	global r, background, label, button, timer

	if paused:
		r["bg"] = "green"
		label["bg"] = "green"
		button["bg"] = "green"
		timer["bg"] = "green"
	else:
		r["bg"] = "orange"
		label["bg"] = "orange"
		button["bg"] = "orange"
		timer["bg"] = "orange"


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


def send_notification():
	global paused

	if paused:
		Popen(
			"notify-send 'Stop, take a break!'", 
			stdin=PIPE, 
			stdout=PIPE, 
			stderr=PIPE
		)
	else:
		Popen(
			"notify-send 'Time is up, folk! Get back to work!'", 
			stdin=PIPE, 
			stdout=PIPE, 
			stderr=PIPE
		)


def win():
	global w, r, label_text, button_text, timer_text, label, button, timer, minutes_passed, seconds_passed

	w = Window(
		window_name="Pomodoro",
		window_size="200x100",
		window_icon="./tomato.png"
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
	global r, minutes_passed, seconds_passed, paused, timer_text

	while True:
		if r is not None:
			if paused:
				toggle_bg()
			else:
				seconds_passed -= 1

				s = seconds_passed

				if seconds_passed <= 0:
					minutes_passed -= 1
					seconds_passed = 59

				if seconds_passed < 10:
					s = f"0{seconds_passed}"

				timer_text.set(f"{minutes_passed}:{s}")
				
				if minutes_passed <= 0:
					minutes_passed = float(pause_interval)
					toggle_pause()
					send_notification()
				toggle_bg()

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
