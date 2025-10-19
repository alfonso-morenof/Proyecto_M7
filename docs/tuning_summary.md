# Tuning de Hiperparámetros – Resumen

- **Semilla**: **60**
- **Métrica**: **F1-macro** (cv=5)
- **Mejor F1 (cross-val)**: **0.8627**
- **Mejores parámetros**:

```json
{
  "clf": "LogisticRegression",
  "clf_params": {
    "C": 1.0,
    "class_weight": "balanced",
    "dual": false,
    "fit_intercept": true,
    "intercept_scaling": 1,
    "l1_ratio": null,
    "max_iter": 1000,
    "multi_class": "deprecated",
    "n_jobs": null,
    "penalty": "l2",
    "random_state": 60,
    "solver": "liblinear",
    "tol": 0.0001,
    "verbose": 0,
    "warm_start": false
  },
  "clf__C": 5,
  "tfidf__max_df": 0.9,
  "tfidf__max_features": 30000,
  "tfidf__min_df": 3,
  "tfidf__ngram_range": [
    1,
    1
  ]
}
```

## Top-10 combinaciones (ordenadas por rank)

|   rank_test_score |   mean_test_score |   std_test_score | param_clf                                                                   |   param_clf__C | param_tfidf__ngram_range   |   param_tfidf__min_df |   param_tfidf__max_df |   param_tfidf__max_features |
|------------------:|------------------:|-----------------:|:----------------------------------------------------------------------------|---------------:|:---------------------------|----------------------:|----------------------:|----------------------------:|
|                 1 |          0.862738 |       0.00447548 | LogisticRegression(class_weight='balanced', max_iter=1000, random_state=60, |              5 | (1, 1)                     |                     3 |                  0.95 |                       30000 |
|                   |                   |                  |                    solver='liblinear')                                      |                |                            |                       |                       |                             |
|                 1 |          0.862738 |       0.00447548 | LogisticRegression(class_weight='balanced', max_iter=1000, random_state=60, |              5 | (1, 1)                     |                     3 |                  0.95 |                       40000 |
|                   |                   |                  |                    solver='liblinear')                                      |                |                            |                       |                       |                             |
|                 1 |          0.862738 |       0.00447548 | LogisticRegression(class_weight='balanced', max_iter=1000, random_state=60, |              5 | (1, 1)                     |                     3 |                  0.9  |                       40000 |
|                   |                   |                  |                    solver='liblinear')                                      |                |                            |                       |                       |                             |
|                 1 |          0.862738 |       0.00447548 | LogisticRegression(class_weight='balanced', max_iter=1000, random_state=60, |              5 | (1, 1)                     |                     3 |                  0.9  |                       30000 |
|                   |                   |                  |                    solver='liblinear')                                      |                |                            |                       |                       |                             |
|                 5 |          0.86091  |       0.00405637 | LogisticRegression(class_weight='balanced', max_iter=1000, random_state=60, |              5 | (1, 1)                     |                     2 |                  0.9  |                       30000 |
|                   |                   |                  |                    solver='liblinear')                                      |                |                            |                       |                       |                             |
|                 5 |          0.86091  |       0.00405637 | LogisticRegression(class_weight='balanced', max_iter=1000, random_state=60, |              5 | (1, 1)                     |                     2 |                  0.9  |                       40000 |
|                   |                   |                  |                    solver='liblinear')                                      |                |                            |                       |                       |                             |
|                 5 |          0.86091  |       0.00405637 | LogisticRegression(class_weight='balanced', max_iter=1000, random_state=60, |              5 | (1, 1)                     |                     2 |                  0.95 |                       40000 |
|                   |                   |                  |                    solver='liblinear')                                      |                |                            |                       |                       |                             |
|                 5 |          0.86091  |       0.00405637 | LogisticRegression(class_weight='balanced', max_iter=1000, random_state=60, |              5 | (1, 1)                     |                     2 |                  0.95 |                       30000 |
|                   |                   |                  |                    solver='liblinear')                                      |                |                            |                       |                       |                             |
|                 9 |          0.859371 |       0.00352345 | LogisticRegression(class_weight='balanced', max_iter=1000, random_state=60, |              3 | (1, 1)                     |                     3 |                  0.95 |                       30000 |
|                   |                   |                  |                    solver='liblinear')                                      |                |                            |                       |                       |                             |
|                 9 |          0.859371 |       0.00352345 | LogisticRegression(class_weight='balanced', max_iter=1000, random_state=60, |              3 | (1, 1)                     |                     3 |                  0.95 |                       40000 |
|                   |                   |                  |                    solver='liblinear')                                      |                |                            |                       |                       |                             |