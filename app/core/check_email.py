import requests
from django.conf import settings

def check(email):
    try:
        url = "https://api.hunter.io/v2/email-verifier?email={}&api_key={}".format(email, settings.SECRET_KEY_HUNTER)
        res = requests.get(url)
        if 'data' in  res and res['data']['result'] ==  "deliverable":
            return True
        else:
            return False
    except Exception as e:
        raise e