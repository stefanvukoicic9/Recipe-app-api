from django.conf import settings
from pyhunter import PyHunter
from core.models import Owner
import clearbit
from django.conf import settings

def check(email):
    try:
        hunter = PyHunter(settings.SECRET_KEY_HUNTER)
        res = hunter.email_verifier(email)
        
        if res['regexp']:
            return True
        else:
            return False

    except Exception as e:
        return False

def create_owner(user, email):
    city = ''
    state = ''
    photo = ''
    linkedin = ''
    location = ''
    employment_domain = ''
    employment_name = ''
    employment_area = ''
    employment_role = ''
    employment_seniority = ''

    try:
        clearbit.key = settings.SECRET_KEY_CLEARBIT
        response = clearbit.Enrichment.find(email=email)
        
        response = response['person']
        if 'geo' in response and 'city' in response['geo'] and response['geo']['city'] :
            city = response['geo']['city']  
        if 'geo' in response and 'state' in response['geo'] and response['geo']['state'] :
            state = response['geo']['state'] 
        if 'avatar' in response and response['avatar']:
            photo = response['avatar']
        if 'linkedin' in response and 'handle' in response['linkedin'] and response['linkedin']['handle']:
            linkedin= response['linkedin']['handle']
        if 'location' in response:
            location = response['location']
        if 'domain' in response['employment'] and response['employment']['domain']:
            employment_domain= response['employment']['domain']
        if 'name' in response['employment'] and response['employment']['name']:
            employment_name= response['employment']['name']
        if 'title' in response['employment'] and response['employment']['title']:
            employment_area= response['employment']['title']
        if 'role' in response['employment'] and response['employment']['role']:
            employment_role= response['employment']['role']
        if 'seniority' in response['employment'] and response['employment']['seniority']:
            employment_seniority= response['employment']['seniority']       
        return Owner.objects.create(user=user, city = city,state = state, photo = photo, linkedin = linkedin, location=location, employment_domain=employment_domain, \
            employment_name=employment_name, employment_area=employment_area, employment_role=employment_role, employment_seniority=employment_seniority)
    except Exception as e:
        return Owner.objects.create(user=user, city = city,state = state, photo = photo, linkedin = linkedin, location=location, employment_domain=employment_domain, \
            employment_name=employment_name, employment_area=employment_area, employment_role=employment_role,  employment_seniority=employment_seniority)
        