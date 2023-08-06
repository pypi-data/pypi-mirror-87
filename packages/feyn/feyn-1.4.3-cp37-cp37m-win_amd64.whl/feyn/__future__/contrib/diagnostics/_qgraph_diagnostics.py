def _get_graph_diagnostics(graph):
    from numbers import Number
    diag_table = {
        'depth': [],
        'loc': [],
        'sources': [],
        'spec': [],
        'activation': [],
        'state': [],
        'errcode': []
    }
    for id, interaction in enumerate(graph):
        state = interaction.state._to_dict()
        if 'cat' in interaction.spec:
            categories = state['categories']
            ncats = len(categories)
            minw = min(c[1] for c in categories)
            maxw = max(c[1] for c in categories)
            state = {'cats': ncats, 'min': minw, 'max': maxw}

        for key, value in state.items():
            if isinstance(value, Number):
                state[key] = f"{value:.3E}"
        diag_table['state'].append(state)

        diag_table['spec'].append(interaction.spec)
        diag_table['depth'].append(interaction.depth)

        diag_table['activation'].append([f"{act:.3E}" for act in interaction.activation])
        diag_table['loc'].append(id)
        diag_table['sources'].append(interaction.sources)
        diag_table['errcode'].append(interaction._errcode)
    return diag_table


def qgraph_diagnostics(qgraph, fit_df=None, max_graphs=None):
    """Get diagnostics for your QGraph to debug errors or graph behaviour.
    Use fit_df to run in-step fitting for each graph to also diagnose exceptions.

    Arguments:
        qgraph {feyn.QGraph} -- Your QGraph

    Keyword Arguments:
        fit_df {Union(pd.DataFrame, dict(str, np.array))} -- A dataset you'd like to debug for. Either a pandas dataframe or dict of numpy arrays (default: {None})
        max_graphs {int} -- amount of graphs to show for (mostly relevant when not using fit_df) (default: {None})

    Returns:
        [list(dict(str, str))] -- a list of diagnostic objects
    """
    # Make sure we get a new sampling in if this function is called after an error occured and the user wants to reproduce it
    if fit_df is not None:
        qgraph._refresh()

    tables = []
    if max_graphs is None:
        max_graphs = len(qgraph)

    for i, g in enumerate(qgraph[:max_graphs]):
        size = len(g)
        diag_table = {
            'graph_id': [i]*size
        }

        error = ['']*size
        if fit_df is not None:
            try:
                g.fit(fit_df)
            except Exception as e:
                error = [str(e)]*size

        # Check for unexecuted graphs
        elif len(g[0].activation) == 0:
            continue

        graph_diag = _get_graph_diagnostics(g)
        for key, value in graph_diag.items():
            diag_table[key] = value

        diag_table['error'] = error
        tables.append(diag_table)

    return tables
