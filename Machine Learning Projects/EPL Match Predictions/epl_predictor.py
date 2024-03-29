### Import modules and Data ###

import pandas as pd

matches = pd.read_csv("matches.csv", index_col=0)


### Exploring the Data ###

#print(matches.head())
#print(matches.shape)

#print(matches['team'].value_counts())

#print(matches[matches['team'] =='Liverpool'])

#print(matches['round'].value_counts)

#print(matches.dtypes)


### Manipulating Data / Creating Predictors ###

matches['date'] = pd.to_datetime(matches['date'])
#print(matches.dtypes)

matches['venue_code'] = matches['venue'].astype('category').cat.codes
#print(matches)

matches['opp_code'] = matches['opponent'].astype('category').cat.codes
#print(matches)

matches['hour'] = matches['time'].str.replace(':.+', '', regex=True).astype('int')
#print(matches)

matches['day_code'] = matches['date'].dt.dayofweek
#print(matches)


### Defining Target to Predict ###

matches['target'] = (matches['result'] == 'W').astype('int')
#print(matches)


### Create and Train Machine Learning Model ###

from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1)

train = matches[matches['date'] < '2022-01-01']

test = matches[matches['date'] > '2022-01-01']

predictors = ['venue_code', 'opp_code', 'hour', 'day_code']

rf.fit(train[predictors], train['target'])

preds = rf.predict(test[predictors])


### Measuring Accuracy ###

from sklearn.metrics import accuracy_score

acc = accuracy_score(test['target'], preds)
#print(acc)

combined = pd.DataFrame(dict(actual=test['target'], predicted=preds), index=test.index)
#print(pd.crosstab(index=combined['actual'], columns=combined['prediction']))

from sklearn.metrics import precision_score
#print(precision_score(test['target'], preds))


### Improving Accuracy with Rolling Averages ###

grouped_matches = matches.groupby('team')

group = grouped_matches.get_group('Manchester City')
#print(group)

def rolling_averages(group, cols, new_cols):
    group = group.sort_values('date')
    rolling_stats = group[cols].rolling(3, closed='left').mean()
    group[new_cols] = rolling_stats
    group = group.dropna(subset=new_cols)
    return group

cols = ['gf', 'ga', 'sh', 'sot', 'dist', 'fk', 'pk', 'pkatt']
new_cols = [f'{c}_rolling' for c in cols]
# print(new_cols)

rolling_averages(group, cols, new_cols)

matches_rolling = matches.groupby('team').apply(lambda x: rolling_averages(x, cols, new_cols))
#print(matches_rolling)

matches_rolling = matches_rolling.droplevel('team')
#print(matches_rolling)

matches_rolling.index = range(matches_rolling.shape[0])
#print(matches_rolling)


### Retraining Machine Learning Model ###

def make_predictions(data, predictors):
    train = data[data['date'] < '2022-01-01']
    test = data[data['date'] > '2022-01-01']
    rf.fit(train[predictors], train['target'])
    preds = rf.predict(test[predictors])
    combined = pd.DataFrame(dict(actual=test['target'], predicted=preds), index=test.index)
    precision = precision_score(test['target'], preds)
    return combined, precision

combined, precision = make_predictions(matches_rolling, predictors + new_cols)
#print(precision)

combined = combined.merge(matches_rolling[['date', 'team', 'opponent', 'result']], left_index=True, right_index=True)
#print(combined)


### Compare Team predictions across the same game ###

class MissingDict(dict):
    __missing__ = lambda self, key: key

map_values = {
    'Brighton and Hove Albion': 'Brighton',
    'Manchester United': 'Manchester Utd',
    'Newcastle United': 'Newcastle Utd',
    'Tottenham Hotspur': 'Tottenham',
    'West Ham United': 'West Ham',
    'Wolverhampton Wanderers': 'Wolves'
}

mapping = MissingDict(**map_values)
#print(mapping['West Ham United'])
#print(mapping['Arsenal'])

combined['new_team'] = combined['team'].map(mapping)
#print(combined)

merged = combined.merge(combined, left_on=['date', 'new_team'], right_on=['date', 'opponent'])
#print(merged)

print(merged[(merged['predicted_x'] ==1) & (merged['predicted_y'] == 0)]['actual_x'].value_counts())
