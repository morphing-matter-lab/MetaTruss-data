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
        
        
        self.curveWidth = 0.5
        self.shadeAlpha = 0.1
        
        self.tickLength = 1.0
        self.tickWidth = 0.5
        
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
        

    
    def plotCurve(self, x, Y, label="Label", colorIndex=0):
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
        plt.plot(x, y, color=self.colors[colorIndex], label=label, lw=self.curveWidth)
        
        # plot shade
        if nSamples > 1:
            std = Y.std(0)

            lower = y - std
            upper = y + std
            plt.fill_between(x, lower, upper, color=self.colors[colorIndex], alpha=self.shadeAlpha)
    
        
    def show(self, title=None, xLabel=None, yLabel=None,
             folderDir='', save=False,
             legend=True, xLog=False, yLog=False, fullFrame=True,
             xTicks=None, yTicks=None, xFormatterFunc=None, yFormatterFunc=None,
             pad=0.5 ):
    
        # appearance
        plt.tick_params(left="on", bottom="on", direction="in", length=self.tickLength, width=self.tickWidth, labelsize=self.font_size, pad=2)
        
        # Change the frame width
        ax = plt.gca()  # Get the current axes
        if fullFrame:
            frameWidths = [0.5, 0.5, 0.5, 0.5]
        else:
            frameWidths = [0.5, 0.5, 0, 0]
            
        for i, axis in enumerate(['left', 'bottom', 'right', 'top']):
            ax.spines[axis].set_linewidth(frameWidths[i])
        

        if xLog:
            plt.xscale('log')


        # yLog
        if yLog:
            plt.yscale('log')
        
        # legend
        if legend:
            plt.legend(frameon=False, fontsize=self.font_size)
        
        # xTicks and yTicks:
        if xTicks:
            plt.xticks(xTicks[0], xTicks[1])
        
        if yTicks:
            plt.yticks(yTicks[0], yTicks[1])
            # plt.yticks(y_locs, [f'{loc:.3f}' for loc in y_locs])
        
        
        if xFormatterFunc:
            xFormatter = ticker.FuncFormatter(xFormatterFunc)
            plt.gca().xaxis.set_major_formatter(xFormatter)
        
        if yFormatterFunc:
            yFormatter = ticker.FuncFormatter(yFormatterFunc)
            plt.gca().yaxis.set_major_formatter(yFormatter)
        
        
        
        # title and labels
        if title and False: # don't plot title, do it in Figma
            plt.title(title, fontsize=self.font_size)
        if xLabel:
            plt.xlabel(xLabel, fontsize=self.font_size)
        if yLabel:
            plt.ylabel(yLabel, fontsize=self.font_size)
        
        
        # layout
        # plt.tight_layout(pad=pad)
        
        # save
        if save:
            if folderDir[-1] != '/':
                folderDir += '/'
            fileDir = folderDir + title

            os.makedirs(folderDir, exist_ok=True)
            plt.savefig(fileDir)
            print('saved to {}'.format(fileDir))
        
        # plt.show()
        

    