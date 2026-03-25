'''
here is a back end description for creating negotiation session
functions (
create session
update negotiation details
complete session
cancel session
)


'''

from db import URL, HEADERS
import httpx

def create_session(lender_id, borrower_id):
    response = httpx.post(
        f'{URL}/rest/v1/sessions',
        headers = {**HEADERS , 'Prefer': 'return=representation'},
        json = {'lender_id': lender_id, 'borrower_id': borrower_id , 'status' : 'pending'}
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)
    return response.json()[0]

def update_negotiation_details(loan_amount, days, loan_due_date, return_amount):
    response = httpx.patch(
        f"{URL}/rest/v1/sessions",
        headers = {**HEADERS, 'Prefer' : "return=representation"},
        json = {'amount': loan_amount, 'days' : days,
                 "due_date" : loan_due_date,
                  "return" : return_amount}
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)
    return response.json()[0]


# for any sides agreement 
def set_agreement(session_id, role):
    field = f'{role}_agree'
    response = httpx.patch(
        f"{URL}/rest/v1/sessions",
        headers = {**HEADERS , 'Prefer' : 'return=representation'},
        params = {'id': f'eq.{session_id}'},
        json = {field: True}
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)
    return response.json()[0]
def complete_session(session_id):
    response = httpx.patch(
        f'{URL}/rest/v1/sessions',
        headers = HEADERS,
        params = {'id': f'eq.{session_id}'},
        json = {'status' : 'complete'}
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)

def cancel_session(session_id):
    response = httpx.patch(
        f'{URL}/rest/v1/sessions',
        headers = HEADERS,
        params = {'id' : f'eq.{session_id}'},
        json = {'status': 'canceled'}
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)
    
def get_pending_session(borrower_id):
    response = httpx.get(
        f'{URL}/rest/v1/sessions',
        headers = HEADERS,
        params = {
            'borrower_id' : f'eq.{borrower_id}',
            'status' : 'eq.pending',
            'select' : '*'
        }
    )
    data = response.json()
    return data[0] if data else None


def get_session_with_lender (session_id):
    response =httpx.get(
        f"{URL}/rest/v1/sessions",
        headers = HEADERS,
        params  =  {'id' : f'eq.{session_id}', 'select' : '*,users!lender_id(name)'}
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)

    data = response.json()
    return data[0] if data else None
