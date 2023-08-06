import matplotlib.pyplot as plt 
import numpy as np 

class Graphbar:

    def plot_bars_by_group(grouped_data,colors,edgecolor=None,property_name="Data by group",ylabel="Value",figsize=(16,6),annotations = True):
        
        """Make bar graph by group.

        Params:
        ------
        
        grouped_data: (dict) 
            Each key represents a group, each group is a dictionary, where each key is a characteristic with its value.

        colors: (list)
            List with the colors of each characteristic

        edgecolor: (str)
            Color of the border of the rectangle, if it is None the border will be equeal to the color of the rectangle

        property_name: (str) Chart title 

        ylabel: (str) Y axis name

        figsize: (tuple) Chart dimensions

        annotations (boolean) If each bar shows the value

        Output:
        ------

        Bar graph by group
        
        """

        groups = list(grouped_data.keys())
        labels = [list(grouped_data[k].keys()) for k in grouped_data.keys()][0]

        n_groups = len(groups)
        n_labels = len(labels)
        
        width = 1/(n_groups+1)

        # the label locations
        main_x = np.arange(n_labels)
        
        if n_groups % 2 == 0:
            pos = "edge"
        else:
            pos = "center"
        
        X = []
        k = [k if i == 0 else -1*k for k in range(1,n_groups) for i in range(2)] 
        for n in range(n_groups-1):
            X.append([r+k[n]*width for r in main_x])
                            
        fig, ax = plt.subplots()
        fig.set_size_inches(figsize)

        rects = []
        
        for g in range(n_groups):
            if g == 0:
                rects.append(ax.bar(main_x,grouped_data[groups[g]].values(),width=width,label=groups[g],color=colors[g],edgecolor = edgecolor,align=pos))
            else:
                rects.append(ax.bar(X[g-1],grouped_data[groups[g]].values(),width=width,label=groups[g],color=colors[g],edgecolor = edgecolor,align=pos))

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel(ylabel)
        ax.set_title(f'{property_name}')
        if pos == "center":
            ax.set_xticks(main_x)
        else:
            ax.set_xticks(X[0])
        ax.set_xticklabels(labels)
        ax.grid(False)
        ax.legend()

        #add annotations
        if annotations:
            heights = []
            for rect in rects:
                for r in rect:
                    height = r.get_height()
                    ax.annotate('{} '.format(height),
                        xy=(r.get_x() + r.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')