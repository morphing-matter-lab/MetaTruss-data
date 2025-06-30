import os

import scipy.stats as stats
import numpy as np

# define null and Alternative Hypothesis
# H0: mean of all groups are equal
# H1: mean of all groups are not equal
#
# define significance level alpha
alpha = 0.05

# load data from loadData.py
from loadData import data

data = data


# check if the ANOVA assumptions are satisfied
assumptionPassed = True

# check if the variances of all groups are equal
statistic, pvalue = stats.levene(*data)
print('statistic = %.3f, pvalue = %.3f' % (statistic, pvalue))
if pvalue > alpha:
    print('Same variances (fail to reject H0)')
else:
    assumptionPassed = False
    print('Different variances (reject H0)')

# check if population is normal
statistic, pvalue = stats.shapiro(np.concatenate(data))
print('statistic = %.3f, pvalue = %.3f' % (statistic, pvalue))
if pvalue > alpha:
    print('Sample looks Gaussian (fail to reject H0)')
else:
    assumptionPassed = False
    print('Sample does not look Gaussian (reject H0)')

if not assumptionPassed:
    print('Assumptions are not satisfied, use non-parametric test')
    # statistic, pvalue = stats.kruskal(*data)
    # print('statistic = %.3f, pvalue = %.3f' % (statistic, pvalue))
    # if pvalue > alpha:
    #     print('Same distributions (fail to reject H0)')
    # else:
    #     print('Different distributions (reject H0)')
    # exit()

else:
    # calculate degrees of freedom
    dfBetween = len(data) - 1
    dfWithin = 0
    for d in data:
        dfWithin += len(d) - 1
    dfTotal = dfBetween + dfWithin
    
    # calculate eta squared
    ssBetween = statistic * dfBetween
    ssWithin = statistic * dfWithin
    ssTotal = statistic * dfTotal
    etaSquared = ssBetween / ssTotal
    
    # perform one-way ANOVA
    statistic, pvalue = stats.f_oneway(*data)
    print('statistic = %.3f, pvalue = %.3f' % (statistic, pvalue))
    
    print('F(%d, %d) = %.3f, p = %.3f, etaSquared = %.3f' % (dfBetween, dfWithin, statistic, pvalue, etaSquared))
    
    
    # interpret p-value
    if pvalue > alpha:
        print('Same distributions (fail to reject H0)')
    else:
        print('Different distributions (reject H0)')
        
    # perform multiple pairwise comparison (Tukey HSD)
    from scipy.stats import tukey_hsd

    
    res = tukey_hsd(data[0], data[1], data[2], data[3], data[4])
    # res.pvalue
    print(res)
    
    
    # boxplot
    import matplotlib.pyplot as plt

    # fig, ax = plt.subplots(figsize=(2.5, 2.0), dpi=72*5 )
    fig, ax = plt.subplots(figsize=(2.5 * 1.2, 2.2 * 1.2), dpi=72 * 5)
    box = ax.boxplot(data.T, showmeans=True, meanline=True, patch_artist=True)
    
    colors = [
        '#F36C46',
        '#63A5BF',
        '#F6D359',
        '#E33247',
        '#F59B43',
        '#66C8D2'
    ]
    
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)

    # line width and line color
    for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(box[element], color='black', linewidth=0.7)
    
    # Scatter plot of individual data points
    for i, d in enumerate(data):
        # Add some random "jitter" to the x-axis
        x = np.random.normal(i + 1, 0.04, size=len(d))
        ax.scatter(x, d, alpha=0.9, edgecolors='black',linewidths=0.5, color='black', zorder=3, s=5, marker='x')

    frameWidths = [0.5, 0.5, 0, 0]
    for i, axis in enumerate(['left', 'bottom', 'right', 'top']):
        ax.spines[axis].set_linewidth(frameWidths[i])
    
    ax.set_xticklabels(['2', '8', '16', '32', '64'], fontsize=5)
    ax.set_yticklabels(['0', '0.2', '0.4', '0.6', '0.8', '1', '1.2', '1.4'], fontsize=5)
    # ax.set_xlabel('number of channels', fontsize=5)
    # ax.set_ylabel('HV score', fontsize=5)


    plt.tick_params(left="on", bottom="on", direction="in", 
                    length=0.5 * 4, 
                    width=0.5, 
                    labelsize=6 * 0.75,
                    pad=2)
    
    
    
    # plt.tight_layout(pad=0.5)

    os.makedirs('./output', exist_ok=True)
    plt.savefig('./output/ANOVA.svg')
    # plt.show()
    
    
    
    
    
        
    
    



