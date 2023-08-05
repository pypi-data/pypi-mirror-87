# -*- coding:utf-8 -*-
__author__ = 'yangjian'
"""

"""

# -*- coding:utf-8 -*-
__author__ = 'yangjian'
"""

"""
from sklearn.metrics import matthews_corrcoef, make_scorer
from sklearn.model_selection import train_test_split
from tabular_toolbox.datasets.dsutils import load_bank
from tabular_toolbox.drift_detection import DriftDetector

matthews_corrcoef_scorer = make_scorer(matthews_corrcoef)


df = load_bank().head(10000)
y = df.pop('y')
X_train, X_test = train_test_split(df, train_size=0.7, shuffle=True, random_state=9527)
dd = DriftDetector()
dd.fit(X_train, X_test)

assert len(dd.feature_names_) == 17
assert len(dd.feature_importances_) == 17
assert dd.auc_
assert len(dd.estimator_) == 5
