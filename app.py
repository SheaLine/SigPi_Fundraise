from flask import Flask,redirect,request
import stripe
import os
app = Flask(__name__, static_url_path= "", static_folder="public")

test_price = 'price_1NkxgQHiDjhflRKUYpjQ981z'
recur_test_price = 'price_1NkxlUHiDjhflRKUbOY9YThZ'
live_price = 'price_1N4C4rHiDjhflRKUQtRNAGAz'
recur_live_price = 'price_1N4CcAHiDjhflRKUmVIdrS7l'


stripe.api_key = 'sk_test_51N4BDbHiDjhflRKUHquvU8LYLFJCyhfvMn6LzQP0Z7vRVGsebsW9647AKj24Jrp8175s6BjCfP1KAMZt2gXPjvg900NybbpdFP'#os.environ.get('STRIPE_SECRET_KEY')
YOUR_DOMAIN = "http://127.0.0.1:5000"

@app.route('/')
def home():
	return app.send_static_file('index.html')

@app.route('/create-checkout-session',methods=['POST'])
def create_checkout_session():
	payment_type = request.form.get('payment_type')
	try:
		if payment_type == "one_time":
			price_id = test_price
			mode = "payment"
		elif payment_type == "monthly":
			price_id = recur_test_price
			mode = "subscription"
		else:
			return "Invalid payment type", 400

		checkout_session = stripe.checkout.Session.create(
			line_items = [
				{
					'price': price_id,
					'quantity': 1
				}
			],
			mode = mode,
			success_url= YOUR_DOMAIN + "/success.html",
			cancel_url = YOUR_DOMAIN + "/index.html"
		)
	except Exception as e:
		return str(e)


	return redirect(checkout_session.url, code = 303)
if __name__ == "__main__":
	app.run(debug = True)
	