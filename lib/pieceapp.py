import os
os.chdir('/src/notebooks')
import ipywidgets as widgets
import numpy as np
import IPython.display as Disp
import matplotlib.pyplot as plt
import chess
import chess.svg
import chess.polyglot
import io

class IndexTracker:

    def __init__(self, X, white, black):
        self.label = white + " vs " + black
        self.fig, ax = plt.subplots(1, 1)
        self.ax = ax
        ax.set_title(self.label)
        self.X = X
        rows, cols, self.slices = 300,300,self.X.shape[2]
        self.ind = 0 # self.slices//2
        self.scroll = self.fig.canvas.mpl_connect('scroll_event', self.onscroll)
        self.im = ax.imshow(self.X[:, :, self.ind],cmap='gray')
        button1 = widgets.Button(description=">>>")
        button2 = widgets.Button(description="<<<")
        buttonsB = widgets.VBox(children=[button2])
        buttonsW = widgets.VBox(children=[button1])
        all_widgets = widgets.HBox(children=[buttonsB,buttonsW])
        display(all_widgets)
        self.update()
        button1.on_click(self.log1)
        button2.on_click(self.log2)

        
    def log1(self, b):
        if self.ind < self.X.shape[2]-1:
            self.ind = (self.ind + 1) % self.slices
        self.update()

    def log2(self, b):
        if self.ind > 0:
            self.ind = (self.ind - 1) % self.slices
        self.update()
        
    def onscroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        self.im.set_data(self.X[:, :, self.ind])
        self.im.axes.figure.canvas.draw()
        
        
        
        

        

        
        
        
