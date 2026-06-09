import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error

df = pd.read_csv("data/cleaned/model_data.csv")
df = df.dropna()

drop_cols = ['match_id', 'match_date', 'match_round', 'venue_name',
             'match_home_team', 'match_away_team', 'home_margin']

for test_year in [2021, 2022, 2023, 2024]:
    train = df[df['match_date'] < f'{test_year}-01-01']
    test = df[(df['match_date'] >= f'{test_year}-01-01') & 
              (df['match_date'] < f'{test_year+1}-01-01')]
    
    x_train = train.drop(columns=drop_cols)
    y_train = train['home_margin']
    x_test = test.drop(columns=drop_cols)
    y_test = test['home_margin']
    
    model = xgb.XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1)
    model.fit(x_train, y_train)
    
    preds = model.predict(x_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    accuracy = ((preds > 0) == (y_test > 0)).mean()
    print(f"{test_year} — MAE: {mae:.2f}, RMSE: {rmse:.2f}, Accuracy: {accuracy:.1%}")

train_final = df[df['match_date'] < '2025-01-01']
test_final = df[df['match_date'] >= '2025-01-01']

x_train_final = train_final.drop(columns=drop_cols)
y_train_final = train_final['home_margin']
x_test_final = test_final.drop(columns=drop_cols)
y_test_final = test_final['home_margin']

model.fit(x_train_final, y_train_final)
preds_final = model.predict(x_test_final)

mae = mean_absolute_error(y_test_final, preds_final)
rmse = np.sqrt(mean_squared_error(y_test_final, preds_final))
accuracy = ((preds_final > 0) == (y_test_final > 0)).mean()

print(f"\n2025 Test MAE: {mae:.2f}, RMSE: {rmse:.2f}, Accuracy: {accuracy:.1%}")