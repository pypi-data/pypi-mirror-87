"""
Functions for creating a partial dependence plot of an Abzu graph.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import feyn
from typing import Iterable, Optional
from collections.abc import Iterable 

def _cartesian_product(arrays) -> np.ndarray:
    #Find the unique combination of all values
    la = len(arrays)
    dtype = np.result_type(*arrays)
    arr = np.empty([len(a) for a in arrays] + [la], dtype=dtype)
    for i, a in enumerate(np.ix_(*arrays)):
        arr[...,i] = a
    return arr.reshape(-1, la).T

def _update_with_cartesian_product( samples ):
    #Apply cartesian to samples
    value_arr = []
    column_arr = []
    for key, value in samples.items():
        column_arr.append(key)
        value_arr.append(value)

    total_df = _cartesian_product(value_arr)

    for idx, col in enumerate(column_arr):
        samples[ col ] = total_df[ idx ].astype(samples[col].dtype)

def _create_by_samples( data: np.ndarray, n_samples: int = 100 ) -> np.ndarray:
    #Let the "by" variable vary from min to max of the variables values
    if data.dtype == 'object':
        return np.unique(data)

    return np.linspace(np.min(data), np.max(data), n_samples)


def _create_samples( data: np.ndarray ) -> np.ndarray:
    #Find fixed values for remaining features in graph.

    #For catgorical features apply the 3 most frequent categories
    if data.dtype == 'object':
        cats, counts = np.unique(data, return_counts = True)
        return cats[np.argsort(-counts)][:3]
      
    else:
        #For numerical features find the the 10, 50 and 90 percentiles
        rounded_quantiles = [np.round(np.quantile(data, x), 2) for x in [0.1, 0.5, 0.9]]
        return np.unique(rounded_quantiles)


def _to_numpy_array( something ):
    #Fix formatting
    
    # something is str
    if isinstance(something, str):
        return np.array([something] , dtype="object")
    
    # something is iterable
    if isinstance(something, Iterable):
        
        # something is an iterable of stings
        if isinstance(something[0], str):
            return np.array(something , dtype="object")
        # not an iterable of strings
        return np.array(something)
    
    return np.array([something])

def plot_partial(graph:feyn.Graph, data:Iterable, by:str, fixed:Optional[dict] = None) -> None:
   
    """
    Plot a partial dependence plot. 

    This plot is useful to interpret the effect of a specific feature on the model output.

    Example:
    > qg = qlattice.get_regressor(["age","smoker","heartrate"], output="heartrate")
    > qg.fit(data)
    > best = qg[0]
    > feyn.__future__.contrib.inspection._partial_dependence.plot_partial_dependence(best, data, by="age")

    You can use any column in the dataset as the `by` parameter.
    If you use a numerical column, the feature will vary from min to max of that varialbe in the training set.
    If you use a categorical column, the feature will display all categories, sorted by the average prediction of that category.

    Arguments:
        graph -- The graph to plot.
        data -- The dataset to measure the loss on.
        by -- The column in the dataset to interpret by.
        fixed -- A dictionary of features and associated values to hold fixed
    """

    # Accept pandas dataframes
    if type(data).__name__ == "DataFrame":
        data = { col: data[col].values for col in data.columns }

    # Ensure fixed is a dict with numpy arrays
    fixed = {
        key: _to_numpy_array(val) \
            for key, val in fixed.items()
    } if fixed is not None else {}
   
    #Point to the target
    target = graph.target

    #Point to features in the chosen graph that for our plots needs to be fixed
    cols = [ col for col in graph.features if col not in [by] ]
    
    
    samples = {
        col : fixed[col] if col in fixed else _create_samples(data[col]) \
            for col in cols
    }
    
    samples[by] = _create_by_samples(data[by])
    _update_with_cartesian_product(samples)
    
    # Make unique ids for each combination of fixed values for plotting
    samples['id'] = ''
    first=True
    for col in cols:
        
        if first:
            first = False
        else:
            samples['id'] = np.char.add(samples['id'], ', ')
        
        if samples[col].dtype == 'object':
            samples['id'] = np.char.add(samples['id'], samples[col].astype('U'))

        else:
            samples['id'] = np.char.add(samples['id'], np.round(samples[col],2).astype('U'))
            
    # Perform predictions on the new values
    samples['preds'] = graph.predict(samples)

    #palette = plt.get_cmap('tab20')
    number_of_colors = 8
    palette = ListedColormap(list(feyn.plots._themes.AbzuColors._abzu_colors.values())[:number_of_colors])

    linestyles = ['-', '--', ':', '-.']
    markerstyles = ["o", "v", "s", "P"]
    
    #Start plotting inputs
    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    spacing = 0.005
    
    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom + height + spacing, width, 0.2]
    rect_histy = [left + width + spacing, bottom, 0.2, height]

    # Set rectangular Figure
    plt.figure(figsize=(8, 8))

    ax_scatter = plt.axes(rect_scatter)
    ax_scatter.tick_params(direction='in', top=True, right=True)
    ax_histx = plt.axes(rect_histx)
    ax_histx.tick_params(direction='in', labelbottom=False)
    ax_histy = plt.axes(rect_histy)
    ax_histy.tick_params(direction='in', labelleft=False)

    import pandas as pd

    total_df = pd.DataFrame(samples).sort_values( by='id' )

    legend_text = ', '.join(cols)
    
    #Distinguish between numerical and categorical plots
    if data[by].dtype == 'object':
        
        sort_df = total_df.groupby(by).agg(preds_sort = ('preds', 'mean')).reset_index().sort_values('preds_sort')

        total_df = pd.merge(total_df, sort_df, on = by, suffixes = (False, False)).sort_values('preds_sort')

        plot_df = pd.merge(pd.DataFrame(data), sort_df, on = by, suffixes = (False, False)).sort_values('preds_sort')

        support = plot_df[target]
        ax_scatter.scatter(support, plot_df[by], alpha = 0.3, color = 'grey', label='_nolegend_')
        
        for i, group in enumerate(total_df.id.sort_values().unique()):
            #print(total_df[total_df.id == group])
            scatter_df = total_df[total_df.id == group]
            ax_scatter.scatter(scatter_df['preds'], scatter_df[by], color = palette(i%number_of_colors), marker=markerstyles[(i//number_of_colors) - (i//(number_of_colors*len(markerstyles))*len(markerstyles))], label = group)
        ax_scatter.set_xlabel(f"Predicted {target}")
        ax_scatter.legend(title = legend_text, loc='center left', bbox_to_anchor=(1.35, 0.5))
        ax_scatter.set_ylabel(by)

        ax_histx.hist(support, bins=30, color = 'grey', rwidth=0.9, alpha =.6)
        
        x, ind, height = np.unique(plot_df[by], return_counts=True, return_index=True)
        ax_histy.barh(x[np.argsort(ind)], height[np.argsort(ind)], color = 'grey', alpha =.6)
        
        #ax_histy.hist(data[by], color = 'grey', rwidth=0.9, alpha =.6, orientation='horizontal')

        ax_histy.set_xticklabels("")

        plt.show()
        
    else:
        support = data[target]
        ax_scatter.scatter(data[by], support, alpha = 0.3, color = 'grey')

        for i, group in enumerate(total_df.id.unique()):
            line_df = total_df[total_df.id == group].sort_values(by)
            ax_scatter.plot(line_df[by], line_df['preds'], color = palette(i%number_of_colors), linestyle=linestyles[(i//number_of_colors) - (i//(number_of_colors*len(linestyles))*len(linestyles))], label = group, linewidth = 1.5)
        ax_scatter.set_xlabel(by)
        ax_scatter.set_ylabel(f"Predicted {target}")
        ax_scatter.set_title(f"'{by}' on '{target}'")
        ax_scatter.legend(title = legend_text, loc='center left', bbox_to_anchor=(1.35, 0.5))
        
        ax_histx.hist(data[by], bins=30, color = 'grey', rwidth=0.9, alpha =.6)
        ax_histy.hist(support, bins=30, color = 'grey', rwidth=0.9, alpha =.6, orientation='horizontal')
        
        ax_histx.set_xlim(ax_scatter.get_xlim())
        ax_histy.set_ylim(ax_scatter.get_ylim())
        
        plt.show()