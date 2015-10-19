'''
Paypal payment test script
'''

import paypalrestsdk


CID = "AcmyU6YTlL9WatGsFOcCJjbXIqj0RwIvt7UAZwwUW1-XkUD59ofWwb3Ps1i6iHIuw2Wgw9AY3mHYyEOa"
SECRET = "ELNECBlmyyU60DXH3os0GUYx9nTKhgkoQewlJwImBrk40odCyIwBYNwbWDLqWmCQJBIM5Rfr7VhHVxX6"


result = paypalrestsdk.configure({
    'mode': 'sandbox',
    'client_id': CID,
    'client_secret': SECRET
});

payment = paypalrestsdk.Payment({
    "intent": "sale",
    "payer": {
        "payment_method": "paypal",
    },
    "transactions": [{
        # "item_list": {
        #     "items": [{
        #         "name": "item",
        #         "sku": "item",
        #         "price": "1.00",
        #         "currency": "USD",
        #         "quantity": 1
        #     }]
        # },
        "amount": {
            "total": "1.00",
            "currency": "USD"
        },
        "description": "This is the payment transaction description."
    }],
    "redirect_urls": {
        "return_url": "http://127.0.0.1:8000/payment/paypal/?success=true",
        "cancel_url": "http://127.0.0.1:8000/payment/paypal/?cancel=true"
    }
})

if payment.create():
    print "Payment created successfully", payment
    for link in payment.links:
        if link.method == "REDIRECT":
            print link.href
else:
    print(payment.error)
