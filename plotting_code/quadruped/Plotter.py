import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as ticker
import seaborn as sns
import tqdm

        
class Plotter:
    def __init__(
            self,
            width=6,
            height=4,
            width_px=None,
            height_px=None,
            ppi=72,
            digits=1
        ):
        
        sns.set_theme(style="white")
        matplotlib.rcParams['font.family'] = 'sans-serif'
        matplotlib.rcParams['font.sans-serif'] = 'Helvetica Neue'
        
        self.colors = [
            '#F21365',
            '#48C288',
            '#F1B807',
            '#63A5BF',
            '#F27A5E',
            '#F5AB55',
        ]

        self.line_width = 0.5
        self.font_size = 6 * 0.75
        self.digits = digits
        
        # Convert pixels to inches if pixel dimensions are provided
        if width_px is not None and height_px is not None:
            width = width_px / ppi
            height = height_px / ppi
        
        plt.figure(figsize=(width, height))


    def plot(self, x, Y, label="Label", colorIndex=0):
        # x: values for x axis [nx, ]
        # Y: values for y axis [nSamples, nY]
        
        # preprocessing data
        assert(x.ndim == 1 and Y.ndim == 2)
        nSamples = Y.shape[0]       # if nSamples is 1, no std plotted, others std plotted
        
        if nSamples == 1:   # no std, directly plot Y
            y = Y.reshape(-1)
        else:   # plot mean and std
            y = Y.mean(0)
        
        # plot
        plt.plot(x, y, color=self.colors[colorIndex], label=label, linewidth=self.line_width)
        
        if nSamples > 1:
            std = Y.std(0)
            lower = y - std
            upper = y + std
            plt.fill_between(x, lower, upper, color=self.colors[colorIndex], alpha=.1, linewidth=self.line_width)
    
    def scatter(self, labels, X, Y):
        
        plt.scatter(X, Y)
        for i, label in enumerate(labels):
            plt.text(X[i]- 5, Y[i]+ 0.2, label)
    
    def plot5bars(self, X):
        plt.bar([0, 1, 2, 3, 4], X, color=self.colors[:5])
        
    def show(self, title, xAxis="xAxis", yAxis="yAxis", legend=True, folderDir='', save=False):

        # plt.yscale('log')

        # plt.title(title)
        
        # plt.xlabel(xAxis)
        # plt.ylabel(yAxis)
        
        # appearance
        plt.tick_params(left="on", bottom="on", direction="in", 
                        length=self.line_width * 4, 
                        width=self.line_width, 
                        labelsize=self.font_size,
                        pad=2)
        
        # Change the frame width
        ax = plt.gca()  # Get the current axes
        for axis in ['top', 'bottom', 'left', 'right']:
            ax.spines[axis].set_linewidth(self.line_width) 
        
        
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.' + str(self.digits) +'f'))
        
        if legend:
            plt.legend(frameon=False, 
                  fontsize=self.font_size,  # Smaller than default
                  handlelength=1.5,               # Length of legend lines
                  handletextpad=0.5,              # Space between line and text
                  columnspacing=1.0,              # Space between columns
                  borderpad=0.2)                  # Padding inside legend
        
        if save:
            if folderDir[-1] != '/':
                folderDir += '/'
            fileDir = folderDir + title
            os.makedirs(folderDir, exist_ok=True)
            plt.savefig(fileDir, bbox_inches='tight', dpi=300)
            print('saved to {}'.format(fileDir))
        
        # plt.show()
        

    