from flask import Flask, render_template, request # type: ignore
import numpy as np # type: ignore
import pickle

app = Flask(__name__)

# Load the trained Random Forest model
with open('creditcard.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route("/", methods=["GET", "POST"])
def fraud_detection():
    prediction_message = ""  # Default empty message

    if request.method == "POST":
        # Collect input values from form
        input_data = [
            float(request.form["distance_from_home"]),
            float(request.form["distance_from_last_transaction"]),
            float(request.form["ratio_to_median_purchase_price"]),
            int(request.form["repeat_retailer"]),
            int(request.form["used_chip"]),
            int(request.form["used_pin_number"]),
            int(request.form["online_order"])
        ]
        
        # Convert to numpy array and reshape for prediction
        input_array = np.array(input_data).reshape(1, -1)
        
        # Get prediction (1 = Fraud, 0 = Legitimate)
        prediction = int(model.predict(input_array)[0])

        # Set prediction message based on result
        if prediction == 1:
            prediction_message = "🚨 Fraudulent Transaction Detected!"
        else:
            prediction_message = "✅ Transaction is Secure."

    return render_template("index.html", prediction_message=prediction_message)  # Pass the message

if __name__ == "__main__":
    app.run(debug=True)
