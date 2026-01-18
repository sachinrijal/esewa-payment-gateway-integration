import base64
import json
from django.contrib import messages
from django.shortcuts import redirect, render
import requests
from payment.models import Donation

def home(request):

    data = request.GET.get('data')

    if data :

        decoded_data = base64.b64decode(data).decode('utf-8')   # Decode the data
        data_dict = json.loads(decoded_data)    
        total_amount = data_dict['total_amount'] 
        transaction_uuid = data_dict['transaction_uuid']
        product_code = data_dict['product_code']

        
        url = "https://rc.esewa.com.np/api/epay/transaction/status/"

        params = {
            "product_code": "EPAYTEST",
            "total_amount": total_amount,
            "transaction_uuid": transaction_uuid
        }

        response = requests.get(url, params=params, timeout=10)

        data = response.json()

        status = data.get("status")


        if status == "COMPLETE" :
            messages.success(request , f'payment has been confirmed ')
            Donation.objects.filter(transaction_uuid=transaction_uuid).update(status=True)
        else:
            messages.error(request,'payment hasnot been confirmed ')

        return redirect('home')


    return render(request,'index.html')
