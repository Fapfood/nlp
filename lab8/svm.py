from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


def prepare_svm(set_kind, part_kind):
    with open('{}/{}-data.txt'.format(set_kind, part_kind), encoding='utf8') as f:
        data = f.read().splitlines()

    with open('{}/{}-label.txt'.format(set_kind, part_kind), encoding='utf8') as f:
        label = f.read().splitlines()

    return data, label


pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', OneVsRestClassifier(LinearSVC())),
])
parameters = {
    'tfidf__max_df': (0.25, 0.5, 0.75),
    'tfidf__ngram_range': [(1, 1), (1, 2), (1, 3)],
    "clf__estimator__C": [0.01, 0.1, 1],
    "clf__estimator__class_weight": ['balanced', None],
}
grid_search_tune = GridSearchCV(
    pipeline, parameters, cv=2, n_jobs=2, verbose=3)

train_x, train_y = prepare_svm('train', '1')
test_x, test_y = prepare_svm('test', '1')
grid_search_tune.fit(train_x, train_y)
best_clf = grid_search_tune.best_estimator_
predictions = best_clf.predict(test_x)

print(classification_report(test_y, predictions))
