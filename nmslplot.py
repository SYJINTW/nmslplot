import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from pathlib import Path
from statistics import mean
import matplotlib.pyplot as plt

# color
color_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
errorbar_color = "#3A3A3A"

# font
csfont = {'family':'Times New Roman', 'serif': 'Times' , 'size' : 20}
plt.rc('text', usetex=True)
plt.rc('font', **csfont)

# bar plot size
bar_width = 0.4
bar_btw_space = 0.04
bar_space = 0.2

# errorbar plot size
err_lw=1.5
err_capsize=4
err_capthick=1.5

# set fig size
figsize=(6.4, 4.8)

def nmslBarPlot(df, x, y, hue="", 
                xlim = "", ylim = "", 
                xlabel = "", ylabel = "", 
                loc='lower right', 
                savePlot = False, showPlot = False, showResults = True,
                saveDir = "", saveImgName = ""):
    
    plt.figure(figsize=figsize)
    
    # don't change
    # =========================================================
    categories = df[x].unique()
    
    hues = []
    if hue:
        hues = df[hue].unique()
        hues.sort()
        # print(hues)
        
        # decide the bars location
        x_axis = np.arange(len(categories)) * (len(hues)*bar_width + (len(hues)-1)*bar_btw_space + bar_space)
        x_axis_offset = np.arange((len(hues)-1)*((bar_width/2)+(bar_btw_space/2))*(-1), (len(hues))*(bar_width/2), bar_width + bar_btw_space)
    else:
        x_axis = np.arange(len(categories)) * (bar_width + bar_space)
        
    # bar lists
    bars = []

    if hue:
        all_means = []
        all_stds = []
        all_cis = []
        for hue_value in hues:
            value_means = []
            value_stds = []
            value_cis = []
            for category in categories:
                filtered_df = df[df[x] == category]
                filtered_df = filtered_df[filtered_df[hue] == hue_value]
                
                mean = filtered_df[y].mean()
                
                # Calculate standard deviation
                std = filtered_df[y].std(ddof=1)  # use ddof=1 for sample standard deviation
                
                # # Calculate the 95% confidence interval using the t-distribution
                # n = len(df)
                # t_value = stats.t.ppf(0.975, n-1)  # use 0.975 for a two-tailed test
                # ci_offset = t_value * (std / (n**0.5)) * 2
                
                # Calculate the confidence interval (95%)
                sem = stats.sem(filtered_df[y])
                ci = stats.t.interval(0.95, len(filtered_df[y])-1, loc=np.mean(filtered_df[y]), scale=sem)
                ci_offset = ci[1] - mean
                
                value_means.append(mean)
                value_stds.append(std)
                value_cis.append(ci_offset)

            all_means.append(value_means)
            all_stds.append(value_stds)
            all_cis.append(value_cis)
        
        if showResults:
            print(f"categories: {categories}")
            print(f"hues: {hues}")
            print(f"mean: {value_means}")
            print(f"std: {value_stds}")
            print(f"ci: {value_cis}")

        for idx in range(len(hues)):
            bars.append(plt.bar(x_axis+x_axis_offset[idx], all_means[idx], yerr=all_cis[idx], \
                                error_kw=dict(lw=err_lw, capsize=err_capsize, capthick=err_capthick, ecolor=errorbar_color), \
                                width=bar_width, color=color_palette[idx]))

    # -------------------------------- without hue ------------------------------- #
    else:
        value_means = []
        value_stds = []
        value_cis = []
        for category in categories:
            filtered_df = df[df[x] == category]
            
            mean = filtered_df[y].mean()
            
            # Calculate standard deviation
            std = filtered_df[y].std(ddof=1)  # use ddof=1 for sample standard deviation
            
            # # Calculate the 95% confidence interval using the t-distribution
            # n = len(df)
            # t_value = stats.t.ppf(0.975, n-1)  # use 0.975 for a two-tailed test
            # ci_offset = t_value * (std / (n**0.5)) * 2

            # Calculate the confidence interval (95%)
            sem = stats.sem(filtered_df[y])
            ci = stats.t.interval(0.95, len(filtered_df[y])-1, loc=np.mean(filtered_df[y]), scale=sem)
            ci_offset = ci[1] - mean

            value_means.append(mean)
            value_stds.append(std)
            value_cis.append(ci_offset)
        
        if showResults:
            print(f"categories: {categories}")
            print(f"mean: {value_means}")
            print(f"std: {value_stds}")
            print(f"ci: {value_cis}")
        
        # # testing
        # value_cis = [20, 2.516685584318424, 2.438033275506282, 2.4103036018749524, 2.305076802098602]

        bars.append(plt.bar(x_axis, value_means, yerr=value_cis, \
                            error_kw=dict(lw=err_lw, capsize=err_capsize, capthick=err_capthick, ecolor=errorbar_color), \
                            width=bar_width, color=color_palette[0]))

    plt.xticks(x_axis, categories)
    
    # =========================================================
    
    # Showing setting
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if hue:
        plt.legend(bars, hues, title='', loc=loc)
    # plt.title("Template") // usually don't use in paper
    
    if savePlot:
        # create saveDir
        if saveDir:
            saveDir.mkdir(exist_ok=True, parents=True)
        else:
            saveDir = Path(".")
        plt.savefig(f'{saveDir}/{saveImgName}.eps', dpi=300, pad_inches=0, bbox_inches='tight')
        plt.savefig(f'{saveDir}/{saveImgName}.png', dpi=300, pad_inches=0, bbox_inches='tight')
                        
    # Show the plot
    if showPlot:
        plt.show()
    plt.clf()