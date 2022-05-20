import uuid
import requests
import random
from phonenumber_field.phonenumber import PhoneNumber

SMS_API_DOMAIN = "https://smsplus.sslwireless.com"
SSLCARE_SMS_API_KEY = "API_KEY" 
SID = "SID"
SMS_URL = f"{SMS_API_DOMAIN}/api/v3/send-sms"
BULK_SMS_URL = f"{SMS_API_DOMAIN}/api/v3/send-sms/bulk"
DYNAMIC_SMS_URL = f"{SMS_API_DOMAIN}/api/v3/send-sms/dynamic"


def get_random_csmsid(s=9, comb=str(uuid.uuid4())):
    random_data = "".join(random.choices(
        comb, k=s))
    random_string = str(random_data)
    return random_string


def single_sms(phone_number, sms):
    data = {
        "api_token": SSLCARE_SMS_API_KEY,
        "sid": SID,
        "msisdn": phone_number,
        "sms": sms,
        "csms_id": get_random_csmsid()
    }
    headers = {"Content-Type": "application/json",
               "Content-Length": str(len(data)),
               "accept": "application/json"}
    response = requests.post(SMS_URL, json=data, headers=headers)
    print(response.json())


def bulk_sms(phone_number_array, sms):
    data = {
        "api_token": SSLCARE_SMS_API_KEY,
        "sid": SID,
        "msisdn": phone_number_array,
        "sms": sms,
        "batch_csms_id": get_random_csmsid()
    }
    headers = {"Content-Type": "application/json",
               "Content-Length": str(len(data)),
               "accept": "application/json"}
    response = requests.post(BULK_SMS_URL, json=data, headers=headers)
    print(response.json())


def dynamic_sms(phone_number_sms_array):
    data = {
        "api_token": SSLCARE_SMS_API_KEY,
        "sid": SID,
        "sms": phone_number_sms_array,
    }
    headers = {"Content-Type": "application/json",
               "Content-Length": str(len(data)),
               "accept": "application/json"}
    response = requests.post(DYNAMIC_SMS_URL, json=data, headers=headers)
    print(response.json())


class SMSBackendLive:
    def __init__(self, dynamic=False, bulk=False):
        self.bulk = bulk
        self.dynamic = dynamic
        self.sms_queue = None if not dynamic else []

    def add(self, phone_number, sms):
        if isinstance(phone_number, PhoneNumber):
            phone_number = str(phone_number)
        if isinstance(phone_number, str) and len(phone_number) == 14 and phone_number.startswith('+880'):
            self.sms_queue = (phone_number, sms)
        else:
            raise Exception('Invalid phone number!!!')

    def add_bulk(self, phone_number_array, sms):
        phone_numbers = []
        for phone_number in phone_number_array:
            if isinstance(phone_number, PhoneNumber):
                phone_number = str(phone_number)
            if isinstance(phone_number, str) and len(phone_number) == 14 and phone_number.startswith('+880'):
                phone_numbers.append(phone_number)
            else:
                raise Exception('Invalid phone number!!!')
        self.sms_queue = (phone_numbers, sms)

    def add_dynamic(self, phone_number, sms):
        if isinstance(phone_number, PhoneNumber):
            phone_number = str(phone_number)
        if isinstance(phone_number, str) and len(phone_number) == 14 and phone_number.startswith('+880'):
            self.sms_queue.append(
                {"msisdn": phone_number, "text": sms, "csms_id": get_random_csmsid()})
        else:
            raise Exception('Invalid phone number!!!')

    def send(self):
        if self.dynamic:
            dynamic_sms(self.sms_queue)
        elif self.bulk:
            bulk_sms(*self.sms_queue)
        else:
            single_sms(*self.sms_queue)

# sms_gateway = SMSBackendLive()
# sms_gateway.add("+8801682834837", "Test")
# sms_gateway.send()

# sms_gateway = SMSBackendLive(bulk=True)
# sms_gateway.add_bulk(["+8801682834837", "+8801978834837"], "Test")
# sms_gateway.send()

# sms_gateway = SMSBackendLive(dynamic=True)
# sms_gateway.add_dynamic("+8801682834837", "Test1")
# sms_gateway.add_dynamic("+8801978834837", "Test2")
# sms_gateway.send()
