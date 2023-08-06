import itertools
import numpy as np
import matplotlib.pyplot as plt
import feyn
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.model_selection import RepeatedKFold, RepeatedStratifiedKFold


def get_model(model):
    """Gets a linear regression, decision tree or qlattice
    for training.

    Arguments:
        model {Union(str, feyn.QLattice)} -- The desired model, can be 'linear',
        'tree' or feyn.QLattice object
    """

    if isinstance(model, feyn.QLattice):
        return model
    elif model == 'tree':
        return DecisionTreeRegressor(random_state=0)
    elif model == 'linear':
        return LinearRegression()
    else:
        raise ValueError("Analysis can only be done on 'linear', 'tree' or a feyn.QLattice object!")


def repeated_kfold_regression_analysis(data,
                                       target,
                                       model,
                                       n_splits=3,
                                       n_repeats=10,
                                       random_state=None,
                                       qlattice_updates=15,
                                       stypes={}):
    """Repeates a k-fold cross-validation test for either a
    Linear model, a Decision Tree or the QLattice. Idea of usage
    is to check whether data has any signal.

    Arguments:
        data {DataFrame} -- dataset to be analyzed
        target {str} -- output variable of dataset
        model {str} -- type of model; can be 'linear', 'tree' or feyn.QLattice object

    Keyword Arguments:
        n_splits {int} -- number of splits in a single k-fold round (default: {3})
        n_repeats {int} -- total number of k-fold rounds (default: {10})
        random_state {int} -- random state of the repeated k-fold split (default: {None})
        qlattice_updates {int} -- number of QLattice updates (default: {15})
        stypes {dict} -- semantical types for the QLattice (default: {dict()})
    """

    # Separating input from output -- needed by sklearn
    X = data.drop(target, axis=1).copy()
    y = data[target]

    f_model = get_model(model)

    rkf = RepeatedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=random_state)

    rkf_res = []
    for train_index, test_index in rkf.split(X, y):
        X_train, y_train = X.iloc[train_index], y.iloc[train_index]
        X_test, y_test = X.iloc[test_index], y.iloc[test_index]

        # Model part:
        if isinstance(f_model, feyn.QLattice):
            train, test = X_train.copy(), X_test.copy()
            train[target], test[target] = y_train, y_test
            f_model.reset()
            qgraph = f_model.get_regressor(train.columns,
                                            target,
                                            max_depth=2,
                                            stypes=stypes)
            for _ in range(qlattice_updates):
                qgraph.fit(train, threads=4)
                f_model.update(qgraph.best())

            r2_train = qgraph[0].r2_score(train)
            r2_test = qgraph[0].r2_score(test)

        else:
            ff_model = f_model.fit(X_train, y_train)

            r2_train = ff_model.score(X_train, y_train)
            r2_test = ff_model.score(X_test, y_test)

        rkf_res.append([r2_train, r2_test])

    return np.asarray(rkf_res).reshape((n_repeats, n_splits, 2))


def plot_kfold_traintest_score_results(rkf_results,
                                       train_lim=(0., 1.),
                                       test_lim=(0., 1.),
                                       figsize=(10, 5),
                                       title='Repeated k-fold results',
                                       ax=None,
                                       **kwargs_plot):
    """Plots the results of train and test scores from the repeated k-fold
    experiment run for any desired model(s).

    Arguments:
        rkf_results {np.ndarray} -- array with k-fold results;
        must be shape (n_repeats, n_splits, 2)

    Keyword Arguments:
        train_lim {tuple} -- plot range limit for training scores (default: {(0., 1.)})
        test_lim {tuple} -- plot range limit for testing scores (default: {(0., 1.)})
        figsize {tuple} -- size of the figure (default: {(10, 5)})
        title {str} -- title of the plot (default: {'Repeated k-fold results'})
        ax {matplotlib.axes._subplots.AxesSubplot} -- axes object (default: {None})
    """

    rkf_mean = np.mean(rkf_results, axis=1)

    if ax is None:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot()

        ax.set_xlim(test_lim)
        ax.set_ylim(train_lim)
        ax.set_xlabel('test set')
        ax.set_ylabel('train set')

        nticks_train = int((max(train_lim) - min(train_lim)) * 10 + 1)
        nticks_test = int((max(test_lim) - min(test_lim)) * 10 + 1)
        ax.set_xticks(np.linspace(test_lim[0], test_lim[1], nticks_test))
        ax.set_yticks(np.linspace(train_lim[0], train_lim[1], nticks_train))
        ax.grid()
        ax.set_title(title)

    ax.scatter(rkf_mean[:, 1], rkf_mean[:, 0], **kwargs_plot)

    return ax


def plot_multiple_kfold_results(rkf_res_list, labels=['linear', 'tree', 'QLattice']):
    """Function to plot multiple kfold analyses results.

    Arguments:
        rkf_res_list {list} -- List of kfold results

    Keyword Arguments:
        labels {list} -- List of labels corresponding to rkf_res_list
        (default: {['linear', 'tree', 'QLattice']})
    """

    marker_list = itertools.cycle(('o', 'D', 's', 'P', 'v', 'X', '^'))

    len_rkfs = len(rkf_res_list)
    # if len_rkfs != len(labels):

    sc_args = {'marker': next(marker_list), 'label': labels[0]}
    ax = plot_kfold_traintest_score_results(rkf_res_list[0], **sc_args)
    for i in range(1, len_rkfs):
        sc_args = {'marker': next(marker_list), 'label': labels[i]}
        ax = plot_kfold_traintest_score_results(rkf_res_list[i], ax=ax, **sc_args)

    ax.legend()

    return ax


# Classification analysis part:
def get_classif_model(model):
    """Gets a linear regression, decision tree or qlattice
    for training.

    Arguments:
        model {Union(str, feyn.QLattice)} -- The desired model,
        can be 'linear', 'tree' or feyn.QLattice object
    """

    if isinstance(model, feyn.QLattice):
        return model
    elif model == 'tree':
        return DecisionTreeClassifier(random_state=0)
    elif model == 'linear':
        return LogisticRegression()
    else:
        raise ValueError("Analysis can only be done on 'linear', 'tree' or a feyn.QLattice object!")


def repeated_kfold_classification_analysis(data,
                                           target,
                                           model,
                                           n_splits=3,
                                           n_repeats=10,
                                           random_state=None,
                                           qlattice_updates=15,
                                           stypes={}):
    """Repeates a k-fold cross-validation test for either a
    Linear model, a Decision Tree or the QLattice. Idea of usage
    is to check whether data has any signal.

    Arguments:
        data {DataFrame} -- dataset to be analyzed
        target {str} -- output variable of dataset
        model {str} -- type of model; can be 'linear', 'tree' or feyn.QLattice object

    Keyword Arguments:
        n_splits {int} -- number of splits in a single k-fold round (default: {3})
        n_repeats {int} -- total number of k-fold rounds (default: {10})
        random_state {int} -- random state of the repeated k-fold split (default: {None})
        qlattice_updates {int} -- number of QLattice updates (default: {15})
        stypes {dict} -- semantical types for the QLattice (default: {dict()})
    """

    # Separating input from output -- needed by sklearn
    X = data.drop(target, axis=1).copy()
    y = data[target]

    f_model = get_classif_model(model)

    rkf = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=random_state)

    rkf_res = []
    for train_index, test_index in rkf.split(X, y):
        X_train, y_train = X.iloc[train_index], y.iloc[train_index]
        X_test, y_test = X.iloc[test_index], y.iloc[test_index]

        # Model part:
        if isinstance(f_model, feyn.QLattice):
            train, test = X_train.copy(), X_test.copy()
            train[target], test[target] = y_train, y_test
            f_model.reset()
            qgraph = f_model.get_classifier(train.columns,
                                            target,
                                            max_depth=2,
                                            stypes=stypes)
            for _ in range(qlattice_updates):
                qgraph.fit(train, threads=4)
                f_model.update(qgraph.best())

            auc_train = roc_auc_score(train[target], qgraph[0].predict(train))
            auc_test = roc_auc_score(test[target], qgraph[0].predict(test))

        else:
            ff_model = f_model.fit(X_train, y_train)

            auc_train = roc_auc_score(y_train, ff_model.predict_proba(X_train)[:, 1])
            auc_test = roc_auc_score(y_test, ff_model.predict_proba(X_test)[:, 1])

        rkf_res.append([auc_train, auc_test])

    return np.asarray(rkf_res).reshape((n_repeats, n_splits, 2))
