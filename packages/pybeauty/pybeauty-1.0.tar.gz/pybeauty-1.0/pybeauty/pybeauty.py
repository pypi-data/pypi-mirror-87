'''

Welcome to PyBeauty

Python Module for beautifully varying RGB colour sets
that can be set as backgrounds anywhere!

For usgae, kindly read the instructions in README.md
available at https://github.com/AbhayTr/PyBeauty.

Optional Parameters that are available are listed below
in @params and have to be passed as a Dictionary (keys as name of
parameters listed in @params and value is your desired choice
according to the options available for that parameter as
specified in @params) which will be the
first parameter for Beauty() constructor.

@params

mode (Optional):

  Specifies colour set in which the colours have to vary.

  Parameter Value Type: str or list.

  Options for mode parameter:
    "dark": Varies the colour in dark colours only (useful for dark mode projects).
    "light": Varies the colour in light colours only (useful for light mode projects).
    [start_rgb, end_rgb]: Varies the colour from start_rgb value (can be from 0 to 255) to end_rgb value (can be from 0 to 255).

  Default Value: "" (i.e. varies from 0 to 255 RGB Values).

start (Optional):

  Specefies colour in RGB format from which colours have to start varying.

  Input type for start parameter: list [R_Value, G_Value, B_Value] (eg. [0, 0, 0] for black).

  Default Value: [0, 0, 0] (for "dark", none or other mode parameter specified) and [255, 255, 255] (for "light" mode parameter specified).

time (Optional):

  Specifies the time in milliseconds after which the colour is changed according to its range.
  Useful for decreasing the time when using on slow hardware for maintaining the smoothness.

  Parameter Value Type: int.

  Default Value: 40 ms (Just perfect for majority hardware types).

So go ahead and enjoy the beauty of time varying RGB colour sets!

© Abhay Tripathi

'''

import random
import threading

class Beauty:

    def __init__(self, parameters, on_new_color):
        self.parameters = parameters
        self.on_new_color = on_new_color
        self.start()

    def change_color(self):
        if self.red_range == 0 and self.green_range == 0 and self.blue_range == 0:
            self.red_range = random.randint(-self.permissible_range, self.permissible_range)
            self.green_range = random.randint(-self.permissible_range, self.permissible_range)
            self.blue_range = random.randint(-self.permissible_range, self.permissible_range)
            if self.red + self.red_range >= self.min and self.red + self.red_range <= self.max and self.green + self.green_range >= self.min and self.green + self.green_range <= self.max and self.blue + self.blue_range >= self.min and self.blue + self.blue_range <= self.max and self.red_range != 0 and self.green_range != 0 and self.blue_range != 0:
                self.terminal_red = self.red + self.red_range
                self.terminal_green = self.green + self.green_range
                self.terminal_blue = self.blue + self.blue_range
            else:
                self.red_range = 0
                self.green_range = 0
                self.blue_range = 0
        else:
            if self.red == self.terminal_red:
                self.red_range = 0
            else:
                if self.red_range < 0:
                    self.red -= 1
                else:
                    self.red += 1
  
            if self.green == self.terminal_green:
                self.green_range = 0
            else:
                if self.green_range < 0:
                    self.green -= 1
                else:
                    self.green += 1
                
            if self.blue == self.terminal_blue:
                self.blue_range = 0
            else:
                if self.blue_range < 0:
                    self.blue -= 1
                else:
                    self.blue += 1

        self.on_new_color([self.red, self.green, self.blue])
        threading.Timer(self.speed, self.change_color).start()

    def start(self):
        mode = ""
        self.speed = 40 / 1000
        start_bg_color = [0, 0, 0]
        if "speed" in self.parameters:
            self.speed = self.parameters["speed"] / 1000
        if "mode" in self.parameters:
            mode = self.parameters["mode"]
        if "start" in self.parameters:
            mode = self.parameters["start"]
        self.permissible_range = 100
        if mode != "":
            self.permissible_range = 30
        self.min = 0
        self.max = 255
        if mode == "dark":
            self.max = 140
        elif mode == "light":
            self.min = 140
        elif type(mode) == list:
            if len(mode) == 2:
                self.min = mode[0]
                self.max = mode[1]
            if min < 0:
                self.min = 0
            if max > 255:
                self.max = 255
        self.red = 0
        self.green = 0
        self.blue = 0
        if mode == "light":
            self.red = 255
            self.green = 255
            self.blue = 255
        if start_bg_color[0] != 0 or start_bg_color[1] != 0 or start_bg_color[2] != 0:
            if start_bg_color[0] < self.min or start_bg_color[1] < self.min or start_bg_color[2] < self.min:
                start_bg_color[0] = min
                start_bg_color[1] = min
                start_bg_color[2] = min
            if start_bg_color[0] > self.max or start_bg_color[1] > self.max or start_bg_color[2] > self.max:
                start_bg_color[0] = max
                start_bg_color[1] = max
                start_bg_color[2] = max
            self.red = start_bg_color[0]
            self.green = start_bg_color[1]
            self.blue = start_bg_color[2]
        self.on_new_color([self.red, self.green, self.blue])
        self.red_range = 0
        self.green_range = 0
        self.blue_range = 0
        self.terminal_red = 0
        self.terminal_green = 0
        self.terminal_blue = 0
        self.change_color()