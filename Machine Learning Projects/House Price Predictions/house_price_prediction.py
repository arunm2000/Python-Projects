import pandas as pd

fed_files = ["MORTGAGE30US.csv", "RRVRUSQ156N.csv", "CPIAUCSL.csv"]

dfs = [pd.read_csv(f, parse_dates=True, index_col=0) for f in fed_files]

fed_data = pd.concat(dfs, axis=1)

fed_data = fed_data.ffill()

zillow_files = ["Metro_median_sale_price_uc_sfrcondo_week.csv", "Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_month.csv"]

dfs = [pd.read_csv(f) for f in zillow_files]

dfs = [pd.DataFrame(df.iloc[0,5:]) for df in dfs]

for df in dfs:
    df.index = pd.to_datetime(df.index)
    df['month'] = df.index.to_period('M')

price_data = dfs[0].merge(dfs[1], on='month')

price_data.index = dfs[0].index

del price_data['month']
price_data.columns = ['price', 'value']

fed_data = fed_data.dropna()

from datetime import timedelta

fed_data.index = fed_data.index + timedelta(days=2)

price_data = fed_data.merge(price_data, left_index=True, right_index=True)

price_data.columns = ["interest", "vacancy", "cpi", "price", "value"]

import matplotlib.pyplot as plt

price_data["adj_price"] = price_data['price']/price_data['cpi'] * 100

price_data["adj_value"] = price_data['value']/price_data['cpi'] * 100

price_data["next_quarter"] = price_data["adj_price"].shift(-13)

price_data.dropna(inplace=True)

price_data["change"] = (price_data['next_quarter'] > price_data['adj_price']).astype(int)

predictors = ["interest", "vacancy", "adj_price", "adj_value"]
target = "change"

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np

START = 260
STEP = 52

def predict(train, test, predictors, target):
    rf = RandomForestClassifier(min_samples_split=10, random_state=1)
    rf.fit(train[predictors], train[target])
    preds = rf.predict(test[predictors])
    return preds

def backtest(data, predictors, target):
    all_preds = []
    for i in range(START, data.shape[0], STEP):
        train = price_data.iloc[:i]
        test = price_data.iloc[i:(i+STEP)]
        all_preds.append(predict(train, test, predictors, target))

    preds = np.concatenate(all_preds)
    return preds, accuracy_score(data.iloc[START:][target], preds)

yearly = price_data.rolling(52, min_periods=1).mean()

yearly_ratios = [p + "_year" for p in predictors]
price_data[yearly_ratios] = price_data[predictors]/yearly[predictors]

preds, accuracy = backtest(price_data, predictors + yearly_ratios, target)

print(accuracy)

# pred_match = (preds == price_data[target].iloc[START:])
# pred_match[pred_match == True] = "green"
# pred_match[pred_match == False] = "red"
#
# plot_data = price_data.iloc[START:].copy()
# plot_data.reset_index().plot.scatter(x="index", y="adj_price", color=pred_match)
# plt.show()

from sklearn.inspection import permutation_importance
rf = RandomForestClassifier(min_samples_split=10, random_state=1)
rf.fit(price_data[predictors], price_data[target])

result = permutation_importance(rf, price_data[predictors], price_data[target], n_repeats=10, random_state=1)

print(result["importances_mean"])
print(predictors)
