import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import joblib

data = pd.read_csv('loan_data.csv')
X = data[['gender', 'married', 'education', 'employed', 'income', 'loan_amount']]
y = data['loan_status'] 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ikkada version fix kosam ee parameters
model = XGBClassifier(max_depth=5, learning_rate=0.1, n_estimators=100, eval_metric='logloss')
model.fit(X_train, y_train)

joblib.dump(model, 'xgb_model.pkl')
print("Model trained and saved successfully as 'xgb_model.pkl'!")