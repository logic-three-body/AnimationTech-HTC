import os

import numpy as np
from sklearn.ensemble import ExtraTreesRegressor


def reach_train_value_function(X_train, y_train, PRE_COMPUTE_TABLE_INDICES, reshape_dim):
    if X_train.shape[0] == 0:
        return np.zeros((reshape_dim, reshape_dim), dtype=np.float32)
    n_jobs = int(os.environ.get("ANIMATIONTECH_TREE_N_JOBS", "1") or "1")
    model = ExtraTreesRegressor(n_estimators=25, random_state=None, n_jobs=n_jobs)
    model.fit(X_train, y_train)
    preds = model.predict(PRE_COMPUTE_TABLE_INDICES)
    return preds.reshape(reshape_dim, reshape_dim)
