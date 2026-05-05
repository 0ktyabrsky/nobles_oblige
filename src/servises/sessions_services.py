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
client = httpx.AsyncClient()

async def create_session(lender_id, borrower_id, amount, days, amount_return):
    response = await client.post(
        f'{URL}/rest/v1/rpc/create_application_session',
        headers =HEADERS,
        json = {'p_lender_id': lender_id,
                'p_borrower_id': borrower_id,
                'p_amount' :amount,
                'p_days' : days,
                'p_return': amount_return})
    print('STATUS', response.status_code)
    print('BODY', response.text)
    return response.json()

async def update_negotiation_details(session_id, loan_amount, days, loan_due_date, return_amount, updated_by):
    response = await client.patch(
        f"{URL}/rest/v1/sessions",
        headers = {**HEADERS, 'Prefer' : "return=representation"},
        params = {'id': f"eq.{session_id}"},
        json = {'amount': loan_amount,
                 'days' : days,
                 "due_date" : loan_due_date,
                  "return" : return_amount,
                  'last_updated_by': updated_by}
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)
    return response.json()[0]
# joining to session function, to update sessing borrower or lender active column
async def update_session(session_id, role):
    field = f'{role}_active'
    response = await client.patch(
        f"{URL}/rest/v1/sessions",
        headers= {**HEADERS, 'Prefer' : 'return=representation'},
        params = {'id' : f'eq.{session_id}'},
        json = {field: True}
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)
    return response.json()[0]
# leaving session (lender or borrower)
async def deactivate_session(session_id, role):
    field = f"{role}_active"
    response = await client.patch(
        f"{URL}/rest/v1/sessions",
        headers = {**HEADERS, 'Prefer' : 'return=representation'},
        params = {'id': f'eq.{session_id}'},
        json = {field : False}
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)
    return response.json()[0]

# for any sides agreement 
async def set_agreement(session_id, role):
    field = f'{role}_agree'
    response = await client.patch(
        f"{URL}/rest/v1/sessions",
        headers = {**HEADERS , 'Prefer' : 'return=representation'},
        params = {'id': f'eq.{session_id}'},
        json = {field: True}
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)
    return response.json()[0]

async def complete_session(session_id):
    response = await client.patch(
        f'{URL}/rest/v1/sessions',
        headers = HEADERS,
        params = {'id': f'eq.{session_id}'},
        json = {'status' : 'complete'}
    )
    print('CREATE SESSION STATUS', response.status_code)
    print('CREATE SESSION BODY', response.text)

async def cancel_session(session_id):
    response = await client.patch(
        f'{URL}/rest/v1/sessions',
        headers = HEADERS,
        params = {'id' : f'eq.{session_id}'},
        json = {'status': 'canceled'}
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)
# get single session 
async def get_session(session_id):
    response = await client.get(
        f"{URL}/rest/v1/sessions",
        headers = HEADERS,
        params = {
            'id' : f"eq.{session_id}",
            'select' : '*'
        }
    )
    print('GET_SESSION STATUS', response.status_code)
    print('GET SESSION BODY', response.text)
    data = response.json()
    return data[0] if data else None

async def get_pending_session(borrower_id):
    response = await client.get(
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


async def get_session_with_lender (session_id):
    response =await client.get(
        f"{URL}/rest/v1/sessions",
        headers = HEADERS,
        params  =  {'id' : f'eq.{session_id}', 'select' : '*,users!lender_id(name)'}
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)

    data = response.json()
    return data[0] if data else None
