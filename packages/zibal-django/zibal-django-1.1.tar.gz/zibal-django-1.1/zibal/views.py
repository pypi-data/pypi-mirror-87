from django.http import HttpResponse, Http404
from django.shortcuts import render
import requests
import json
from .models import PurchaseHistory
from django.shortcuts import redirect
from .utils import zibal
from django.conf import settings
from .zb import Zibal as zb
from django.contrib.auth import get_user_model

User=get_user_model()

merchant = settings.ZIBAL_MERCHANT
callback_url = settings.DOMAIN_ADDRESS_ZIBAL_CALLBACK



def request(request):
    order = request.GET.get('order')
    amount = request.GET.get('amount')
    mobile = request.GET.get('mobile')
    description = request.GET.get('description')

    if amount is None :
        raise Http404

    # if request.method == "POST":
    #     pass
    # else:
    #     raise Http404
    if order is None :
        order=-1

    if request.user.is_authenticated:
        ins = PurchaseHistory.objects.create(user=request.user, amount=amount , order=order)
    else:
        ins = PurchaseHistory.objects.create( amount=amount , order=order)

    data = {}
    data['merchant'] = merchant
    data['callbackUrl'] = callback_url
    data['amount'] = amount
    data['orderId'] = ins.pk
    if mobile is not None:
        data['mobile'] = mobile
    if description is not None:
        data['description'] = description
    # data['multiplexingInfos'] = multiplexingInfos



    url = "https://gateway.zibal.ir/v1/request"
    response = requests.post(url=url, json=data)
    response = json.loads(response.text)

    if str(response['result']) == "100" or str(response['result']) =="201" :
        ins.trackId = str(response['trackId'])
        ins.result = str(response['result'])
        ins.message = str(response['message'])
        ins.save()

        start_pay_url = "https://gateway.zibal.ir/start/" + ins.trackId
        return redirect(start_pay_url)
    else:
        return HttpResponse("خطایی رخ داده ، لطفا با پشتیبانی تماس بگیرید")

def back(request):
    if request.GET.get('success') == '1':
        trackId = request.GET.get('trackId')
        orderId = request.GET.get('orderId')
        try:
            ins = PurchaseHistory.objects.get(trackId=trackId , pk = orderId , is_paid=False )
        except:
            try:
                ins = PurchaseHistory.objects.get(trackId=trackId, pk=orderId, is_paid=True)
                return render(request, 'verify.html',
                              context={'error': False, 'message': "شما این پرداخت را انجام داده اید"})
            except:
                pass
            return render(request , 'verify.html' , context={'error' : True , 'message' : "تراکنش شما یافت نشد"})

        data = {}
        data['merchant'] = merchant
        data['trackId'] = ins.trackId
        url = "https://gateway.zibal.ir/v1/verify"
        response = requests.post(url=url, json=data)
        response = json.loads(response.text)

        ins.paidAt = response['paidAt']
        ins.cardNumber = str(response['cardNumber'])
        ins.status = str(response['status'])
        ins.amount = str(response['amount'])
        ins.refNumber = str(response['refNumber'])
        ins.result = str(response['result'])
        ins.message = str(response['message'])
        ins.is_call_verify = True
        ins.is_paid = True
        ins.save()
        zibal(ins.order)
        return render(request, 'verify.html', context={'error':False , 'message': "پرداخت شما با موفقیت صورت گرفت . با تشکر"})

    else:
        return render(request, 'verify.html', context={'error': True, 'message': "تراکنش شما موفق نبود"})


def testzb(request):
    order = request.GET.get('order')
    amount = request.GET.get('amount')
    mobile = request.GET.get('mobile')
    description = request.GET.get('description')
    callback_url = "http://127.0.0.1:8000/zibal/callback/"
    zb_obj = zb(merchant)
    data = zb_obj.request(callback_url ,order , amount , mobile , description , request.user )
    print(data)
    if data['status'] == "successful":
        return redirect(data['start_pay_url'])
    else:
        return HttpResponse(data["message"])

def testback(request):
    zb_obj = zb(merchant)
    data = zb_obj.callback(request)
    purchase_history_object = data["PurchaseHistory"]
    if data['status'] == "successful":
        return HttpResponse(data['message'])
    else:
        return HttpResponse(data["message"])
