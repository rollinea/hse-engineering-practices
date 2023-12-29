from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.metrics import roc_auc_score, log_loss

def create_model(solver='liblinear'):
    return LogisticRegression(solver='liblinear')

def cv(X_train, y_train):
    model = create_model()
    param_search = {'C' : [0.001, 0.01, 0.1, 1.], 'penalty': ['l2']}

    splits = TimeSeriesSplit(n_splits=3)
    clf = GridSearchCV(estimator=model, cv=splits,
                            param_grid=param_search, verbose=10, scoring=['roc_auc', 'neg_log_loss'], refit="neg_log_loss")
    clf.fit(X_train, y_train)
    return clf