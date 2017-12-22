from flask import Flask, render_template, request
import braintree

braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    'qr7h9y9634y43hy3',
    '8wtdvybw5yht6crc',
    'c3bf46039e4b5589f65a5b1235c07857'
)

app = Flask(__name__)

@app.route("/")
def index():
    client_token = braintree.ClientToken.generate()
    # return client_token
    return render_template('index.html', client_token=client_token)

@app.route("/checkout", methods=["POST"])
def checkout():
    payment_method_nonce = request.form["payment_method_nonce"]
    email = request.form["email"]
    first_name = request.form["first_name"]
    amount = request.form["amount"]

    result = braintree.Transaction.sale({
        'amount': amount,
        'payment_method_nonce': payment_method_nonce,
        'order_id' : 'Mapped to PayPal Invoice Number',
        'customer': {
            'email': email,
            'first_name': first_name
        },
        "device_data": request.form["data_collector"],
        "options": {
            "three_d_secure": {
                "required": True
            },
             "paypal": {
                "custom_field" : "PayPal custom field",
                "description" : "Description for PayPal email receipt",
            },
        }
    })

    # return payment_method_nonce
    # result = braintree.Transaction.sale({
    #     'amount':'10',
    #     'payment_method_nonce':payment_method_nonce,
    #     'customer': {
    #         'first_name':first_name,
    #         'email':email
    #     }
    # })

    return render_template('checkout.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)
