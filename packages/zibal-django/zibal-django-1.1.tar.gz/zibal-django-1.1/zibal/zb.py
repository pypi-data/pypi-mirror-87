import requests
import json
from .models import PurchaseHistory
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

User=get_user_model()


class Zibal():
    def __init__(self , merchant ):
        self.merchant = merchant

    def request_result(self, result):
        switcher = {
            100: "با موفقیت تایید شد.",
            102: "merchant یافت نشد.",
            103: "Mamerchant غیرفعالrch",
            104: "merchant نامعتبر",
            201: "قبلا تایید شده.",
            105: "amount بایستی بزرگتر از 1,000 ریال باشد.",
            106: "callbackUrl نامعتبر می‌باشد. (شروع با http و یا https)",
            113: "amount مبلغ تراکنش از سقف میزان تراکنش بیشتر است.",
        }
        return switcher.get(result, "خطا در پرداخت")

    def verify_result(self, result):
        switcher = {
            100: "با موفقیت تایید شد.",
            102: "merchant یافت نشد.",
            103: "Mamerchant غیرفعالrch",
            104: "merchant نامعتبر",
            201: "قبلا تایید شده.",
            202: "سفارش پرداخت نشده یا ناموفق بوده است.",
            203: "trackId نامعتبر می‌باشد.",
        }
        return switcher.get(result, "خطا در پرداخت")

    def request(self ,callback_url , order_number , amount_RIAL , mobile , description , user_id=None):

        try:
            user = User.objects.get(pk=user_id)
            ins = PurchaseHistory.objects.create(user = user, amount = amount_RIAL, order = order_number)
        except:
            ins = PurchaseHistory.objects.create(amount=amount_RIAL, order=order_number)


        data = {}
        print(self.merchant)
        data['merchant'] = self.merchant
        data['callbackUrl'] = callback_url
        data['amount'] = amount_RIAL
        data['orderId'] = ins.pk
        if mobile is not None:
            data['mobile'] = mobile
        if description is not None:
            data['description'] = description
        # data['multiplexingInfos'] = multiplexingInfos

        url = "https://gateway.zibal.ir/v1/request"
        response = requests.post(url=url, json=data)
        response = json.loads(response.text)

        if str(response['result']) == "100" or str(response['result']) == "201":
            ins.trackId = str(response['trackId'])
            ins.result = str(response['result'])
            ins.message = str(response['message'])
            ins.save()

            start_pay_url = "https://gateway.zibal.ir/start/" + ins.trackId
            return {"status": "successful", "start_pay_url": start_pay_url, "code" : 11}

        else:
            res = self.request_result(response['result'] )
            return {"status" : "error" , "message" : res , "code" : 12}


    def callback(self , request):
        if request.GET.get('success') == '1':
            trackId = request.GET.get('trackId')
            orderId = request.GET.get('orderId')
            try:
                ins = PurchaseHistory.objects.get(trackId=trackId, pk=orderId, is_paid=False)
            except:
                try:
                    ins = PurchaseHistory.objects.get(trackId=trackId, pk=orderId, is_paid=True)
                    return {"status": "error", "message": "شما این پرداخت را انجام داده اید", "code" : 21 }

                except:
                    return {"status": "error", "message": "تراکنش شما یافت نشد", "code" : 22 }

            data = {}
            data['merchant'] = self.merchant
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
            res = self.verify_result(response['result'])
            return {"status": "successful", "message": res , "code": 20 , "PurchaseHistory" : ins }


        else:
            return {"status": "error", "message": "تراکنش شما موفق نبود", "code": 23}


