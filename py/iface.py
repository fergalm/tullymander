# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 11:03:35 2021

Interface with Jupyter notebooks.

```
%matplotlib notebook
import iface
iface.setup()

@author: fergal
"""

# from ipdb import set_trace as idebug
# from IPython.display import display
import matplotlib.pyplot as plt
from tully import Tullymander
import numpy as np

# from ipywidgets import interact, fixed
import ipywidgets
import pandas as pd

# def setup(configfile, console):

#     tt = Silly()
#     def on_toggle_button_click(source):
#         with console:
#             print(source)
#             tt.set_colour(source)

#     plat_options = tt.votes.columns
#     buttons = ipywidgets.ToggleButtons(options=plat_options)
#     buttons.observe(on_toggle_button_click, 'value')
#     return [buttons]


def setup(configfile, console):
    tt = Tullymander(configfile, console)

    def on_toggle_button_click(source):
        """This func gets called when the toggle buttons are clicked"""
        selection = source['new']
        tt.selectPlatStyle(selection)

    plat_options = tt.votes.columns
    buttons = ipywidgets.ToggleButtons(options=plat_options)
    buttons.observe(on_toggle_button_click, 'value')

    #Tullymander can't do anything with the button input yet,
    #so it don't display the buttons
    return [tt, console]


class Silly():
    """Used for figuring out the jupyter/ipywidget interactive stuff"""
    def __init__(self):
        self.figure = plt.figure()

        self.updateEvent = 'key_press_event'
        self.figure.canvas.mpl_disconnect(self.updateEvent)
        self.figure.canvas.mpl_connect(self.updateEvent, self)

        self.votes = pd.DataFrame(columns="r g b c m".split())
        self.colour = 'ko-'
        self.plot("blank")

    def __call__(self, event):
        x = event.xdata
        y = event.ydata
        key = event.key
        strr = "%.1f %.1f %s" %(x, y, key)
        self.plot(strr)
        return pd.DataFrame(index=x, columns=['a', 'b', 'c'])

    def set_colour(self, source):
        clr = source['new']
        self.colour = "%so-" %(clr)
        self.plot("")

    def plot(self, title):
        x  = np.arange(10)
        plt.plot(x, x, self.colour)
        plt.title(title)