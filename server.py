from flask import Flask, request, jsonify, render_template
import os
import stripe
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Serve the payment page
@app.route("/")
def home():
    return render_template("payment.html")  # Ensure payment.html is inside the "templates" folder

@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = request.json
        amount = data.get('amount', 5000)  # Default $50.00 (5000 cents)

        # Create a PaymentIntent
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd"
        )

        return jsonify({"clientSecret": payment_intent.client_secret})
    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)

