import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import pickle

# 1. Load the structured loan applicant records
data = pd.read_csv('loan_data.csv')

# 2. Separate independent features from the loan status target variable
X = data[['gender', 'married', 'education', 'employed', 'income', 'loan_amount', 'loan_term', 'credit_history', 'property_area']]
y = data['loan_status']  # 1 = Approved, 0 = Rejected

# 3. Split dataset into training and testing partitions
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Initialize and fit the XGBoost model to mirror performance target settings
model = XGBClassifier(max_depth=5, learning_rate=0.1, n_estimators=100)
model.fit(X_train, y_train)

# 5. Export the trained architecture into a portable pickle asset file
with open('xgb_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Model trained and saved successfully as 'xgb_model.pkl'!")
