import joblib
import xgboost as xgb
from data_collector import collect_all_data
import pandas as pd
from sklearn.preprocessing import LabelEncoder

loaded_model = joblib.load('weights/xgboost_model.pkl')

def get_estimate(city):
    X = get_normal_dataset(city)
    print(X.info())
    y_pred = loaded_model.predict(X)
    return y_pred

def get_normal_dataset(city):
    raw_data = collect_all_data([city])
    raw_data.drop(columns=['average_distance', 'country', 'region','bad_dist_count', 'city'], inplace=True)
    raw_data.dropna(inplace=True)
    
    label_encoder = LabelEncoder()

    raw_data['max_negative'] = label_encoder.fit_transform(raw_data['max_negative'])
    raw_data['max_main'] = label_encoder.fit_transform(raw_data['max_main'])
    raw_data['max_positive'] = label_encoder.fit_transform(raw_data['max_positive'])
    raw_data['place'] = label_encoder.fit_transform(raw_data['place'])

    return raw_data

if __name__ == "__main__":
    print(get_estimate('Таганрог'))
