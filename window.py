#!/usr/bin/python3

import tkinter
from functools import partial
from math import floor
from PIL import Image, ImageTk

# Window mode
WINDOW_HIDDEN: int = 0
WINDOW_NORMAL: int = 1
WINDOW_FULL_SCREEN: int = 2
WINDOW_MATCH_SCREEN: int = 3
# Window position
WINDOW_DEFAULT_POS: int = 0
WINDOW_CENTERED: int = 1
# Window look
WINDOW_NATIVE: int = 0
WINDOW_CUSTOM: int = 1
# Cursors
CURSOR_SQUARED: str = "dotbox"
# Font
FONT_FAMILY = "Arial"
ARIAL_LARGE = (FONT_FAMILY, 25)
ARIAL_MEDIUM = (FONT_FAMILY, 18)
ARIAL_SMALL = (FONT_FAMILY, 15)


class Window:
    __window = None
    __window_title = ""
    __x = None
    __y = None

    def __init__(self, window_name: str = "",
                 window_appearance: int = WINDOW_NATIVE,
                 window_buttons: bool = False,
                 window_mode: int = WINDOW_NORMAL,
                 window_size: str = "500x500",
                 window_position: int = WINDOW_DEFAULT_POS,
                 window_icon: str = ""
        ):
        self.__x = 0
        self.__y = 0
        self.__window = tkinter.Tk()
        self.set_name(window_name)
        self.set_mode(mode=window_mode, size=window_size)
        self.set_look(appearance=window_appearance, buttons=window_buttons, name=window_name)
        self.set_position(position=window_position, size=window_size)
        self.set_icon(icon=window_icon)

    def display(self):
        self.__window.mainloop()

    def dispose(self):
        self.__window.destroy()

    def __grab(self, event):
        self.__x = event.x
        self.__y = event.y

    def __release(self, event):
        self.__x = None
        self.__y = None

    def __move(self, event):
        delta_x = event.x - self.__x
        delta_y = event.y - self.__y
        x = self.__window.winfo_x() + delta_x
        y = self.__window.winfo_y() + delta_y
        self.__window.geometry(f"+{x}+{y}")

    def set_name(self, window_name: str = ""):
        if not window_name:
            window_name = "New Window"

        self.__window.title(window_name)
        self.__window_title = window_name

    def set_mode(self, mode: int = WINDOW_NORMAL, size: str = "500x500"):
        global WINDOW_FULL_SCREEN, WINDOW_HIDDEN, WINDOW_NORMAL

        if mode == WINDOW_NORMAL:
            if ("x" not in size) or (not size):
                raise Exception("Using WINDOW_NORMAL, size parameter must be defined too")

            # Set window size
            self.__window.geometry(size)

        elif mode == WINDOW_FULL_SCREEN:
            self.__window.wm_attributes('-fullscreen', 'true')

        elif mode == WINDOW_HIDDEN:
            self.__window.wm_attributes('-fullscreen', 'true')
            self.__window.wm_state("iconic")

    def set_look(self, appearance: int = WINDOW_NATIVE, buttons: bool = False, name: str = "New Window"):
        global WINDOW_CUSTOM

        if appearance == WINDOW_CUSTOM:
            self.__window.wm_overrideredirect(True)
            self.display_actions_bar(name, buttons)

    def set_position(self, position: int = WINDOW_DEFAULT_POS, size: str = "500x500"):
        global WINDOW_CENTERED

        if position == WINDOW_CENTERED:
            screen_width = self.__window.winfo_screenwidth()
            screen_height = self.__window.winfo_screenheight()

            window_width, window_height = size.split("x")

            screen_width = floor((int(screen_width) - int(window_width)) / 2)
            screen_height = floor((int(screen_height) - int(window_height)) / 2)

            self.__window.geometry(f"+{screen_width}+{screen_height}")

    # doesn't work yet :(
    def set_icon(self, icon: str = ""):
        if not (not icon):
            try:
                """ solution 1
                ico = Image.open(icon)
                photo = ImageTk.PhotoImage(ico)
                self.__window.wm_iconphoto(False, photo)"""

                ico = tkinter.PhotoImage(file=icon)
                """ solution 2
                self.__window.iconphoto(False, ico)"""

                """ solution 3 """
                self.__window.tk.call('wm', 'iconphoto', self.__window, ico)
            except Exception as e:
                print(e)

    def display_actions_bar(self, navbar_title: str = "", navbar_buttons: bool = False):
        global ARIAL_SMALL, CURSOR_SQUARED

        # Window name
        handle = tkinter.Label(
            self.__window,
            text=navbar_title,
            font=ARIAL_SMALL
        )
        handle.pack(side="top", fill="both", pady=5)

        # Drag window functionality
        handle.bind("<ButtonPress-1>", self.__grab)
        handle.bind("<ButtonRelease-1>", self.__release)
        handle.bind("<B1-Motion>", self.__move)

        # Add here your navigation bar components        
        if navbar_buttons:
            # Close window button
            tkinter.Button(
                self.__window,
                width="2",
                text="x",
                bg="#d00",
                fg="#fff",
                justify="center",
                relief="flat",
                cursor=CURSOR_SQUARED,
                command=partial(self.dispose)
            ).pack(anchor="w", side="top")    

    def get_root(self):
        return self.__window