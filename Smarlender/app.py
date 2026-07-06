from flask import Flask, render_template, request
import pickle # <-- idi missing undi
import numpy as np

app = Flask(__name__) # <-- rendu sarlu undi, okkate uncham. template_folder teesesam

# Load the pre-trained XGBoost model
with open('xgb_model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Retrieve input data from the HTML form
        gender = int(request.form['gender'])
        married = int(request.form['married'])
        education = int(request.form['education'])
        employed = int(request.form['employed'])
        income = float(request.form['income'])
        loan_amount = float(request.form['loan_amount'])
        loan_term = float(request.form['loan_term'])
        credit_history = float(request.form['credit_history'])
        property_area = int(request.form['property_area'])

        # Convert fields into a structured numpy array
        features = np.array([[gender, married, education, employed, income,
                              loan_amount, loan_term, credit_history, property_area]])

        # Run classification model prediction
        prediction = model.predict(features)

        if prediction[0] == 1: # <-- [0] add chesa, lekapothe error vastundi
            result = "Loan Approved! (Low-Risk Applicant Profile)"
        else:
            result = "Loan Rejected! (High-Risk Applicant Profile)"

        return render_template('index.html', prediction_text=result)

if __name__ == '__main__':
    app.run(debug=True)