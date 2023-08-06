import pandas as pd
import numpy as np

cell_types = ['linear',
            'multiply',
             'tanh', 
             'gaussian', 
             'sine', 
             'add', 
             'log', 
             'inverse', 
             'exp', 
             "circle",
             "sqrt"]

def _get_interaction_index(interaction):
    return interaction._index

def _get_categories(register):
    return register.state.categories

def _get_register_name(register):
    return register.name

def _is_input_register(interaction):
    return 'in' in interaction.spec[0:2]

def _is_cat_register(interaction):
    return 'cat' in interaction.spec

def _is_output_register(interaction):
    return 'out' in interaction.spec

def _is_register(interaction):
    return (_is_input_register(interaction)) or (_is_output_register(interaction))

def _get_interaction_sources_indices(interaction):

    if len(interaction.sources) == 1:
        return interaction.sources[0]
    else:
        return interaction.sources

def _get_prediction(graph,df):
    return graph.predict(df)

def _get_activation(interaction):

    # activation displays values of weights plus bias. Here we take it way.
    if _is_cat_register(interaction):
        return interaction.activation[0] - interaction.state.bias
    return interaction.activation[0]

def _interaction_is_1d(interaction):
    return len(interaction.sources) == 1

def _interaction_is_2d(interaction):
    return len(interaction.sources) == 2

def _is_last_interaction_before_output(interaction,graph):
    """
    Arguments:
        interaction {[feyn._Interaction]}
        graph {[feyn._Graph]}

    Returns:
        [Bool] -- This returns True if this is the last hidden interaction before the output register
    """

    if _get_interaction_index(interaction) == len(graph) - 2:

        return True

    else:

        return False

def _get_col_name_for_act_df(interaction):
    """
    This gives the names for the columns in the activation dataframe

    Arguments:
        interaction {feyn._Interaction} -- An interaction in a feyn graph

    Returns:
        [string] -- If the activation is an input numerical register then this returns 'interaction.name'+'_stdised'
        If categorical register then returns 'interaction.name'+'_weights'.
        If output register then returns 'graph_output'
        If a hidden interaction then returns cell_type + cell_index
    """

    # If a register
    if len(interaction.name) > 0:

        # If a categorical register
        if _is_cat_register(interaction):

            return interaction.name + '_weights'

        # If the output register
        if _is_output_register(interaction):

            return 'graph_output'

        #If input register
        return interaction.name + '_stdised'

    else:
        # If a hidden interaction

        for cell_type in cell_types:

            if cell_type in interaction.spec:

                index = _get_interaction_index(interaction)

                return cell_type + str(index)

def _get_all_cells(graph):

    return [cell for cell in graph]

def _plot_2d_interaction(act_df,interaction,graph,scaling=None):
    """This plots a 2dimensional hidden interaction from the activation dataset.

    Arguments:
        act_df {pd.DataFrame} -- This is a dataset that is returned from feyn_plots.get_activations_df method
        interaction {feyn._Interaction} -- This is a two dimensional hidden interaction.
        graph {feyn._Graph} -- The graph where the interaction lives.

    Returns:
        plotly.graph_objs._figure.Figure -- This is the 2dimensional plot of the interaction
    """
    import plotly.express as px

    axes = []
    interaction_name = _get_col_name_for_act_df(interaction)
    sources_indices = _get_interaction_sources_indices(interaction)
    if scaling == None:
        scaling = []


    for index in sources_indices:
        # This is the input of the interaction
        source = graph[index]

        # If input is a register then plot the values of register and not the stdised values. Hence different name is used
        if _is_input_register(source):

            source_name = _get_register_name(source)

            if source_name in scaling:

                source_name = _get_col_name_for_act_df(source)

        # Input from another hidden interaction
        else:
            source_name = _get_col_name_for_act_df(source)

        axes.append(source_name)

    # If interaction is last before output then we plot graph output not the output of last hidden interaction
    if _is_last_interaction_before_output(interaction,graph):

        title = 'graph_output activation'

        fig = px.scatter(act_df,x=axes[0],y=axes[1],color='graph_output')

    else:

        title = interaction_name + ' activation'
        fig = px.scatter(act_df,x=axes[0],y=axes[1],color=interaction_name)

    fig.update_layout(title_text = title)

    return fig


def _plot_1d_interaction(act_df,
                         interaction,
                         graph,
                         scaling=None):

    """This plots a 1d hidden interaction from the activation dataset

    Arguments:
        act_df {pd.DataFrame} -- Activation dataset from the get_activations_df method
        interaction {feyn._Interaction} -- 1d interaction
        graph {feyn._Graph} -- THe graph where the 1d interaction lives.

    Returns:
        plotly.graph_objs._figure.Figure -- This is the 1-dimensional plot
    """
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    interaction_name = _get_col_name_for_act_df(interaction)

    source_index = _get_interaction_sources_indices(interaction)

    source = graph[source_index]

    if scaling == None:
        scaling = []

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # If the source in an input register
    if _is_input_register(source):

        source_name = _get_register_name(source)

        # If scaling was requested
        if source_name in scaling:

            # Histogram of scaling/weights
            source_name = _get_col_name_for_act_df(source)

            # display weights and not weiughts + bias on the x axes
            fig.add_trace(go.Histogram(x=act_df[source_name], name=source_name))
            sort_act_df = act_df.sort_values(by=source_name)

        # If scaling was not requested
        else:
            
            # If the register is categorical
            if _is_cat_register(source):

                # No scaling and categorical
                # means no Histogram and to sort the 
                # values by their weights
                source_name = _get_register_name(source)
                sort_act_df = act_df.sort_values(
                    by=_get_col_name_for_act_df(source))

            # If register is not categorical
            else:
                
                # Display actual values and not scaled
                source_name = _get_register_name(source)
                fig.add_trace(go.Histogram(x=act_df[source_name] , name=source_name))
                sort_act_df = act_df.sort_values(by=source_name)

    # If source is not a register
    else:
        
        # Display Histogram and sort by source name
        source_name = _get_col_name_for_act_df(source)
        fig.add_trace(go.Histogram(x=act_df[source_name], name=source_name))
        sort_act_df = act_df.sort_values(by=source_name)

    if _is_last_interaction_before_output(interaction, graph):

        fig.add_trace(go.Scatter(x=sort_act_df[source_name],
                                 y=sort_act_df['graph_output'],
                                 mode='lines',
                                 name='graph_output'),
                      secondary_y=True)

        title = 'graph_output activation'


    else:

        fig.add_trace(go.Scatter(x=sort_act_df[source_name],y=sort_act_df[interaction_name],mode='lines',name='activation'),
                    secondary_y=True)
        title = interaction_name + ' activation'

    fig.update_layout(
        title_text = title,
        xaxis_title = source_name)
    fig.update_yaxes(title_text = 'count', secondary_y = False)
    fig.update_yaxes(title_text = 'activation value', secondary_y = True)

    return fig

def _plot_register(act_df,register):
    """When interaction is a register then this plots the histogram of the values in the activation dataframe.

    Arguments:
        act_df {pd.DataFrame} -- Activation dataset from the get_activations_df
        register {feyn._register} -- Either output or input register

    Returns:
        plotly.graph_objs._figure.Figure -- When the register is an input this returns a Histogram of the values of the input.
        When this is an output this is a histogram of the graph_output values and the actual target value
    """
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    if _is_input_register(register):

        name = _get_register_name(register)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Histogram(x=act_df[name] , name=name))
        fig.update_layout(
            title_text = name + ' distribution',
            xaxis_title = name,
            yaxis_title = 'count'
        )


    elif _is_output_register(register):

        number_of_bins_for_target = 50
        target = _get_register_name(register)

        fig = go.Figure()
        fig.add_trace(go.Histogram(x=act_df['graph_output'],name='graph_output'))
        fig.add_trace(go.Histogram(x=act_df[target],name = target,nbinsx=number_of_bins_for_target))

        fig.update_layout(
            title_text = target + ' and graph_output' + ' distribution',
            xaxis_title = 'values',
            yaxis_title = 'count',
            barmode='overlay'
        )
        fig.update_traces(opacity=0.75)

    return fig


def get_activations_df(dataframe, graph):
    """
    Returns a pandas dataframe of activations of each interaction for a given graph.

    Arguments:
        dataframe {[pd.DataFrame]} -- The datapoints to find the activations of.
        graph {[feyn.Graph]} -- The graph with the interactions.

    Returns:
        [pd.Dataframe] -- Extended original dataframe of feature and activations values.
    """
    df_copy = dataframe.copy()

    cells = _get_all_cells(graph)
    activations = [[] for interaction in cells]

    for i in range(len(df_copy)):

        datapoint = df_copy.iloc[i:i+1]
        _get_prediction(graph,datapoint)

        for j in range(len(cells)):

            interaction = cells[j]
            activation = _get_activation(interaction)
            activations[j].append(activation)

    for i in range(len(cells)):

        interaction = cells[i]
        activation_name = _get_col_name_for_act_df(interaction)
        df_copy.loc[:,activation_name] = activations[i]

    return df_copy


def plot_interaction(graph,interaction,dataframe,scaling = None):
    """
    Plots the activation values of datapoints of an interaction. If the interaction is a register then it plots the distribution of points.

    Arguments:
        graph {[feyn.Graph]} -- The graph to calculate activation values
        interaction {[feyn.Interaction]} -- The interaction to plot
        dataframe {[pd.DataFrame]} -- The datapoints to plot
        scaling {[list of strings]} -- The features that will display scaling on axis

    Returns:
        [plotly.graph_objs._figure.Figure] -- Either a scatter plot of datapoints or a histogram of the feature distribution.
    """

    act_df = get_activations_df(dataframe,graph)

    if _is_register(interaction):

        fig = _plot_register(act_df,interaction)

    elif _interaction_is_1d(interaction):

        fig = _plot_1d_interaction(act_df,interaction,graph,scaling)

    if _interaction_is_2d(interaction):

        fig = _plot_2d_interaction(act_df,interaction,graph,scaling)

    return fig

def plot_categories(register):
    """Plots the weights of each category of a categorical register

    Arguments:
        register {feyn._Regsiter} -- Categorical register

    Returns:
        [plotly.graph_objs._figure.Figure] -- Bar chart of weights
    """
    import plotly.graph_objects as go

    register_name = _get_register_name(register)

    categories = _get_categories(register)
    categories.sort(key=lambda x: x[1])

    cat_names = [cat[0] for cat in categories]
    cat_weights = [cat[1] for cat in categories]

    fig = go.Figure(go.Bar(
            x=cat_weights,
            y=cat_names,
            orientation='h'))

    fig.update_layout(title_text = register_name + ' weights',
                    xaxis_title='Weights',
                    yaxis_title='categories')
    return fig
