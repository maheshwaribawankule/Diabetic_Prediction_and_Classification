from flask import Flask, request, render_template, redirect, url_for, session, send_file
import pickle
import numpy as np
import os


# Initialize Flask application
application = Flask(__name__)
app = application

# Set the secret key for session management (important for security)
app.secret_key = 'your_secret_key'  # Change this to a random secret key in production

# Load the scaler and model from the pickle files
scaler = pickle.load(open("DaibeticPrediction_Major/Model/standardScalar.pkl", "rb"))
model = pickle.load(open("DaibeticPrediction_Major/Model/modelForPrediction.pkl", "rb"))

## Route for homepage (serving index.html)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == "your_username" and password == "your_password":
            session['username'] = username
            print(f"Session set: {session}")  # Debugging line
            return redirect(url_for('dashboard'))
        
        return render_template('signin.html', error='Invalid credentials')
    
    return render_template('signin.html')


# Route for dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Route for handling predictions
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    result = ""
    diabetes_type = ""
    diabetes_level = ""
    username = session.get('username', 'Guest')  # Get username from session

    if request.method == 'POST':
        try:
            # Get inputs from the form and convert them to the appropriate types
            Pregnancies = int(request.form.get("Pregnancies"))
            Glucose = float(request.form.get('Glucose'))
            BloodPressure = float(request.form.get('BloodPressure'))
            SkinThickness = float(request.form.get('SkinThickness'))
            Insulin = float(request.form.get('Insulin'))
            BMI = float(request.form.get('BMI'))
            DiabetesPedigreeFunction = float(request.form.get('DiabetesPedigreeFunction'))
            Age = float(request.form.get('Age'))

            # Transform the input data
            new_data = scaler.transform([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
            # Make the prediction
            predict = model.predict(new_data)

            # Interpret the prediction for diabetes presence
            if predict[0] == 1:
                result = "Diabetic"
                if Age < 30 and BMI < 25:
                    diabetes_type = "Type 1 Diabetes"
                else:
                    diabetes_type = "Type 2 Diabetes"

                if Glucose < 140:
                    diabetes_level = "Low"
                elif 140 <= Glucose <= 199:
                    diabetes_level = "Prediabetic"
                else:
                    diabetes_level = "High"
            else:
                result = "Not Diabetic"
                diabetes_type = "None"
                diabetes_level = "Normal"

        except Exception as e:
            result = f"Error in prediction: {e}"

    return render_template('predictdata.html', result=result, diabetes_type=diabetes_type, diabetes_level=diabetes_level, username=username)

# Route for generating the report
@app.route('/generate_report', methods=['POST'])
def generate_report():
    username = session.get('username', 'Guest')  # Get username from session

    # Get the data from the form
    result = request.form.get('result')
    diabetes_type = request.form.get('diabetes_type')
    diabetes_level = request.form.get('diabetes_level')
    
    # Retrieve input data
    Pregnancies = request.form.get('Pregnancies')
    Glucose = request.form.get('Glucose')
    BloodPressure = request.form.get('BloodPressure')
    SkinThickness = request.form.get('SkinThickness')
    Insulin = request.form.get('Insulin')
    BMI = request.form.get('BMI')
    DiabetesPedigreeFunction = request.form.get('DiabetesPedigreeFunction')
    Age = request.form.get('Age')

    # Create report content in tabular format
    report_content = f"""
    Diabetes Prediction Report
    ===========================
    User: {username}  # Include the username
    
    Predictions:
    +------------------------+-----------------+
    | Diabetes Prediction     | {result}        |
    | Diabetes Type           | {diabetes_type} |
    | Diabetes Level          | {diabetes_level}|
    +------------------------+-----------------+
    
    Input Data:
    +------------------------+-----------------+
    | Pregnancies            | {Pregnancies}   |
    | Glucose                | {Glucose}       |
    | Blood Pressure          | {BloodPressure} |
    | Skin Thickness          | {SkinThickness} |
    | Insulin                | {Insulin}       |
    | BMI                    | {BMI}           |
    | Diabetes Pedigree      | {DiabetesPedigreeFunction} |
    | Age                    | {Age}           |
    +------------------------+-----------------+
    """

    # Save report to a file
    report_file = 'diabetes_prediction_report.txt'
    with open(report_file, 'w') as file:
        file.write(report_content)

    # Send the report file as a downloadable file
    return send_file(report_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
