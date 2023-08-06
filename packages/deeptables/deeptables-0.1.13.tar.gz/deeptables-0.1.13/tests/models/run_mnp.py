# -*- coding:utf-8 -*-
__author__ = 'yangjian'
"""

"""
import pandas as pd
import numpy as np
from hypernets.core.callbacks import SummaryCallback, FileLoggingCallback, EarlyStoppingCallback
from hypernets.core.search_space import HyperSpace, MultipleChoice, Bool, Choice
from hypernets.core.searcher import OptimizeDirection
from hypernets.searchers.mcts_searcher import MCTSSearcher
from sklearn.model_selection import train_test_split

from deeptables.models.hyper_dt import DTModuleSpace, DnnModule, DTFit, HyperDT
from deeptables.utils import consts as DT_consts


def my_space():
    space = HyperSpace()
    with space.as_default():
        p_nets = MultipleChoice(
            ['dnn_nets', 'linear', 'fm_nets'], num_chosen_most=2)
        dt_module = DTModuleSpace(
            nets=p_nets,
            auto_categorize=True,  # Bool(),
            cat_remain_numeric=True, # Bool(),
            auto_discrete=Bool(),
            # apply_gbm_features=Bool(),
            # gbm_feature_type=Choice([DT_consts.GBM_FEATURE_TYPE_DENSE, DT_consts.GBM_FEATURE_TYPE_EMB]),
            embeddings_output_dim=Choice([4, 10]),
            embedding_dropout=Choice([0, 0.5]),
            stacking_op=Choice([DT_consts.STACKING_OP_ADD, DT_consts.STACKING_OP_CONCAT]),
            output_use_bias=Bool(),
            apply_class_weight=Bool(),
            earlystopping_patience=Choice([5]))

        dnn = DnnModule(hidden_units=Choice([100, 200]),
                        reduce_factor=Choice([1, 0.8]),
                        dnn_dropout=Choice([0, 0.3]),
                        use_bn=Bool(),
                        dnn_layers=2,
                        activation='relu')(dt_module)
        fit = DTFit(batch_size=Choice([64, 128]))(dt_module)

    return space


rs = MCTSSearcher(my_space, max_node_space=5, optimize_direction=OptimizeDirection.Maximize)
hdt = HyperDT(rs,
              callbacks=[SummaryCallback(), FileLoggingCallback(rs), EarlyStoppingCallback(5, 'max')],
              reward_metric='AUC',
              dnn_params={
                  'hidden_units': ((256, 0, False), (256, 0, False)),
                  'activation': 'relu',
              },
              cache_preprocessed_data=False,
              cache_home='cache')

df = pd.read_csv("mnp_1k.csv", header=None)
df = df.replace(['\\N'], np.nan)

label_index = len(df.columns) - 1
y = df.pop(label_index)

X = df
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12, stratify=y)

hdt.search(X_train, y_train, X_test, y_test, max_trails=50, epochs=2)
