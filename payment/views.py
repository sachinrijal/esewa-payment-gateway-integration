import hmac
import hashlib
import base64
import uuid
from django.shortcuts import render
from .models import Donation  

def generate_signature(key, message):
    key = key.encode('utf-8')
    message = message.encode('utf-8')
    digest = hmac.new(key, message, hashlib.sha256).digest()
    signature = base64.b64encode(digest).decode('utf-8')
    return signature

def payment(request):

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        amount = request.POST.get('amount')

        transaction_uuid = str(uuid.uuid4())
        donation = Donation.objects.create(
            name=name,
            email=email,
            amount=amount,
            transaction_uuid=transaction_uuid,
        )

        
        secret_key = '8gBm/:&EnhH.1/q'
        message = f"total_amount={amount},transaction_uuid={transaction_uuid},product_code=EPAYTEST"
        signature = generate_signature(secret_key,message) 


        context = {
            'name': name,
            'email': email,
            'amount': amount,
            'uuid': transaction_uuid,
            'signature': signature,
        }

        return render(request, "esewa.html", context)

    return render(request, "esewa.html")
