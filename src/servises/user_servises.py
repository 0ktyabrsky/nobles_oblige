
import httpx
from db import URL , HEADERS

def get_user_by_phone(phone):
    response = httpx.get(
        f'{URL}/rest/v1/users',
        headers = HEADERS,
        params = {'phone_number': f'eq.{phone}', 'select': '*'}
    )
    # dubugging
    print('STATUS', response.status_code)
    print('BODY', response.text)
    data = response.json()
    return data[0] if data else None

def create_user(name, phone):
    response = httpx.post(
       f'{URL}/rest/v1/users',
       headers = { **HEADERS, "Prefer" : "retrurn=representation"},
       json = {'name':name,
               'phone_number': phone}
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)

    return response.json()[0]

# gettin user info from db otherwise creating it in db
def get_or_create_user(name, phone):
    record = get_user_by_phone(phone)
    if not record:
        record = create_user(name, phone)
    return record

