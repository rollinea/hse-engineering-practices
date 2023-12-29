import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import hstack

def load_data(data_path):
    columns_to_use = ['date_time', 'zone_id', 'banner_id', 'campaign_clicks',
                      'os_id', 'country_id', 'impressions', 'clicks']
    categorical_columns = ['zone_id', 'banner_id', 'os_id',
                           'country_id', 'impressions', 'clicks']
    data = pd.read_csv(data_path,
                       usecols=columns_to_use,
                       parse_dates=['date_time'])
    data[categorical_columns].astype('category')
    return data


def get_interactions(data, interactions_list):
    for col1, col2 in interactions_list:
        data[f'{col1};{col2}'] = data[col1].astype(str) + "_" + data[col2].astype(str)
    return data

def group_categories(data, column_names, threshold):
    for column in column_names:
        new_value = data[column].max() + 1000
        categories_to_group = data[column].value_counts(normalize=True) < threshold
        categories_to_group = categories_to_group[categories_to_group].index
        data.loc[data[column].isin(categories_to_group), column] = new_value
    return data

def feature_engineering(data, interactions):
    # Удалим nan
    data.dropna(inplace=True)
    
    # Удалим столбец impressions
    data.drop(['impressions'], axis=1, inplace=True)

    # Временные признаки
    data['hour'] = data.date_time.dt.hour
    data['weekday'] = data.date_time.dt.weekday

    # Группировка редких категорий в banner_id, zone_id
    data = group_categories(data, ['banner_id', 'zone_id'], 0.001)

    # Нормировка campaign_clicks
    data['campaign_clicks'] = np.log1p(data.campaign_clicks)

    # Интеракции
    data = get_interactions(data, interactions)

    return data

def create_dataset(data):
    print('Dataset preparation...')
    
    # Train-test split
    ts = pd.Timestamp('2021-10-02 00:00:00')
    data.sort_values(by='date_time', inplace=True)
    train_mask, test_mask = data.date_time < ts, data.date_time >= ts
    X_train, X_test = data[train_mask].copy(), data[test_mask].copy()
    y_train, y_test = X_train.clicks.to_numpy(), X_test.clicks.to_numpy()

    columns_to_drop = ['clicks', 'campaign_clicks', 'date_time']
    train_cc = X_train.campaign_clicks.to_numpy()
    test_cc = X_test.campaign_clicks.to_numpy()
    X_train.drop(columns_to_drop, axis=1, inplace=True)
    X_test.drop(columns_to_drop, axis=1, inplace=True)

    # One hot encoding
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=True)
    X_train = encoder.fit_transform(X_train)
    X_test = encoder.transform(X_test)

    # Add non-categorical features
    X_train = hstack([X_train, train_cc[:, np.newaxis]])
    X_test = hstack([X_test, test_cc[:, np.newaxis]])

    print('Dataset is ready!')

    return X_train, X_test, y_train, y_test


