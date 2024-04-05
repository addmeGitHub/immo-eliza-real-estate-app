Description

Immo Eliza ml is a machine learning model to predict prices of real estate properties in Belgium. The dataset is split by propoerty type into (House) & (Apartment). The ML model is performed only on the (House) data, which is subjected to cleaning and outliers removal. The total record used for ML and prediction is 7931.

For ML several models were experiemented (Linear Regression), (RandomForest) and (GradientBoostingRegressor), but the final model ppicked to predict housing prices in Belgium is (GradientBoostingRegressor) as it provided consistent results.

/Users/ARahim/Documents/GitHub/eliza-deploy/
    ├── api/
    ├── data/
    ├── main.py
    └── train.py
