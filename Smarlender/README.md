# LOAN APPROVAL PREDICTION USING ARTIFICIAL INTELLIGENCE

## 📌 Project Description
This project uses Machine Learning to predict whether a loan application will be approved or not. 
Banks and financial institutions can use this model to automate loan approval decisions and reduce risk.

The model analyzes applicant details like Income, Credit History, Loan Amount, etc. and predicts `Loan_Status: Approved / Not Approved`.

## 🚀 Key Features
- **Data Preprocessing**: Handle missing values, Label Encoding
- **ML Models**: Logistic Regression, RandomForest, Decision Tree comparison
- **Accuracy**: ~85%+ accuracy on test data
- **Web App**: Flask based UI to take user input and predict loan status
- **EDA**: Visualizations for data insights

## 🛠️ Tech Stack
- **Language**: Python 3.10+
- **Backend**: Flask
- **ML Libraries**: Scikit-learn, Pandas, NumPy, Matplotlib, Seaborn
- **Model Saving**: Pickle / Joblib
- **Frontend**: HTML, CSS, Jinja2

## 📊 Dataset Columns
`Loan_ID, Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area, Loan_Status`

Target: `Loan_Status` -> Y = Approved, N = Not Approved

## ⚡ Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Bonasu-lab/Loan-approval-prediction-usinf-Artificial-inteligence.git
    cd Loan-approval-prediction-usinf-Artificial-inteligence
        python -m venv
    venv\Scripts\activate  # For Windows
        pip install -r requirements.txt
            python train.py
                    python app.py
                    ├── data/
│   └── loan_data.csv
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── app.py
├── train.py
├── loan_model.pkl
├── requirements.txt
└── README.md

### **requirements.txt**
```txt
Flask==3.0.0
pandas==2.2.0
numpy==1.26.0
scikit-learn==1.4.0
matplotlib==3.8.0
seaborn==0.13.0
git add README.md requirements.txt
git commit -m "Add professional README and requirements"
git push origin main