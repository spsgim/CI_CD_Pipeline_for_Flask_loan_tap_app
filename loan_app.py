from flask import Flask, request, jsonify
import pickle
import sklearn

app = Flask(__name__)

@app.route("/")
def hello():
    return "<p> Hi! Lovely meeting you!</p>"

@app.route("/ping")
def pinger():
    return "<p> Hello, Thanks for the ping! </p>"

@app.route("/json")
def json_check():
    return {'message': 'Hi I am json!'}

# Load the model once when the application starts
with open('./classifier.pkl', 'rb') as model_pickle:
    clf = pickle.load(model_pickle)

@app.route("/predict", methods=['POST'])
def loan_predict():
    try:
        loan_req = request.get_json()
        if loan_req is None:
            return jsonify({"error": "Invalid input: JSON data is missing"}), 400

        # Validate input data
        required_keys = ['Gender', 'Married', 'ApplicantIncome', 'LoanAmount', 'Credit_History']
        for key in required_keys:
            if key not in loan_req:
                return jsonify({"error": f"Missing data: {key} is required"}), 400

        # Gender is encoded as {'Male': 0, 'Female': 1}
        Gender = 0 if loan_req['Gender'] == 'Male' else 1
        
        # Married is encoded as {'No': 0, 'Yes': 1}
        Married = 1 if loan_req['Married'] == 'Yes' else 0

        ApplicantIncome = loan_req['ApplicantIncome']
        LoanAmount = loan_req['LoanAmount']
        Credit_History = loan_req['Credit_History']

        # Ensure input types are correct
        try:
            ApplicantIncome = float(ApplicantIncome)
            LoanAmount = float(LoanAmount)
            Credit_History = int(Credit_History)
        except ValueError as e:
            return jsonify({"error": f"Invalid input types: {str(e)}"}), 400

        # Make prediction
        result = clf.predict([[Gender, Married, ApplicantIncome, LoanAmount, Credit_History]])

        # Interpret the prediction result
        pred = "Approved" if result[0] == 1 else "Rejected"

        return jsonify({'Your_Loan_Application_is': pred})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
