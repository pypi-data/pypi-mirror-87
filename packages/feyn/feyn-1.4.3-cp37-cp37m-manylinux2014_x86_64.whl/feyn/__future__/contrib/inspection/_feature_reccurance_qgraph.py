import typing

import pandas as pd
import numpy as np
from feyn.filters import MaxEdges

def feature_recurrence_qgraph(train_df, target, qlattice, test_df={}, 
                              filters=[], n_iter=10, stypes:typing.Optional[str] = None,
                              n_fits=10, n_features=1, top_graphs=10,
                              threads=4, get_qgtype='regressor'):
    """Uses the QLattice to extract simple models and
    check which features are the most recurring.
    Arguments:
        train_df {pd.DataFrame} -- training set
        target {str} -- target name
        qlattice {feyn.QLattice} -- the QLattice
    Keyword Arguments:
        test_df -- a test dataset to evalulate on
        filters -- list of filters to apply
        n_iter {int} -- number of full training iterations (default: {10})
        n_fits {int} -- number of updating loops (default: {10})
        n_features {int} -- max number of features, between 1 and 4 (default: {1})
        top_graphs {int} -- number of inspected graphs (default: {10})
        threads {int} -- number of threads (default: {4})
        get_qgtype {str} -- type of qgraph (default: {'regressor'})

    Returns:
        DataFrame that records in features in the top graphs from each iteration
    """
    from sklearn.metrics import roc_auc_score

    if n_features < 1 or n_features > 4:
        raise Exception("Number of features must be between 1 and 4!")
    configurations = {
        1: {'max_depth': 1, 'max_edges': 2},
        2: {'max_depth': 1, 'max_edges': 3},
        3: {'max_depth': 2, 'max_edges': 6},
        4: {'max_depth': 2, 'max_edges': 7}
    }
    max_depth = configurations[n_features]['max_depth']
    max_edges = configurations[n_features]['max_edges']
    res_df = pd.DataFrame()

    if stypes == None:
        stypes = {}

   
    for i in range(n_iter):
        qlattice.reset()
        if get_qgtype == 'regressor':
            qgraph = qlattice.get_regressor(train_df.columns,
                                            target,
                                            max_depth=max_depth,
                                            stypes=stypes)
            if not len(filters) == 0:
                for f in filters:
                    qgraph = qgraph.filter(f)
        elif get_qgtype == 'classifier':
            qgraph = qlattice.get_classifier(train_df.columns,
                                             target,
                                             max_depth=max_depth,
                                             stypes=stypes)
            if not len(filters) == 0:
                for f in filters:
                    qgraph = qgraph.filter(f)
        else:
            raise Exception("QGraph type error: please choose get_type to be \
                either regressor or classifier!")

        qgraph = qgraph.filter(MaxEdges(max_edges))
        for _ in range(n_fits):
            qgraph.fit(train_df, threads=threads)
            best_graphs = qgraph.best()
            qlattice.update(best_graphs)
        # After going through the full update loop,
        # we go through the top 10 graphs
       
        df_tmp = pd.DataFrame()

        for ix, g in enumerate(qgraph[:top_graphs]):

            if not len(test_df) == 0:
                dataset = test_df
            else:
                dataset = train_df
           
            if get_qgtype == 'regressor':
                metric_score = g.r2_score(dataset)
            elif get_qgtype == 'classifier':
                y_pred = g.predict(dataset)
                metric_score = roc_auc_score(dataset[target], y_pred)
               
            df_graph = pd.DataFrame({'iteration': i,
                                  'n_graph': ix,
                                     'n_features': len(g.features),
                                  'features': g.features,
                                   'graph_loss': g.loss_value,
                                  'metric_score': metric_score})
            df_tmp = pd.concat([df_tmp, df_graph], ignore_index=True)
           
        res_df = pd.concat([res_df, df_tmp], ignore_index=True)
    return res_df