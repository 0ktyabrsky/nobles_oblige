import httpx
from db import URL , HEADERS
client = httpx.AsyncClient()


async def insert_loan(lender_id, borrower_id, loan_amount, days, return_amount, due_date,session_id):
    response = await client.post(
        f'{URL}/rest/v1/loans',
        headers = {**HEADERS, 'Prefer' : 'return=representation'},
        json ={
            'lender_id' : lender_id,
            'borrower_id' : borrower_id,
            'amount' : loan_amount,
            'days' : days,
            'return_amount' :return_amount,
            'due_date' : due_date,
            'session_id' : session_id
        } 
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)
    return response.json()[0]


async def get_loans_by_lender(lender_id):
    response = await client.get(
        f"{URL}/rest/v1/loans",
        headers = HEADERS,
        params = {
            'lender_id' : f"eq.{lender_id}",
            'select' : '*,users!fk_borrower_id(name)'
        }
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)
    data = response.json()
    return data if data else []
async def get_loans_by_borrower(borrower_id):
    response = await client.get(
        f"{URL}/rest/v1/loans",
        headers = HEADERS,
        params = {
            'borrower_id' : f'eq.{borrower_id}',
            'select' : '*, users!fk_lender_id(name)'
        }
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)
    data = response.json()
    return data if data else []
async def get_active_loans(borrower_id):
    response = await client.get(
        f'{URL}/rest/v1/loans',
        headers = HEADERS,
        params ={
            'borrower_id': f'eq.{borrower_id}',
            'status' : 'eq.active',
            'select': '*, users!fk_lender_id(name)'
        }
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)
    data = response.json()
    return data if data else []

async def repay_loan( loan_id, borrower_id, return_amount):
    try:
        response = await client.get(
            f'{URL}/rest/v1/users',
            headers = HEADERS,
            params = {
                'id' : f'eq.{borrower_id}',
                'select' : 'balance'

            }
        )
        data = response.json()
        print('STATUS', response.status_code)
        print('BODY', response.text)
        if not data:
            return False, "User not found"
        
        current_balance = float(data[0]['balance'])
        if current_balance < return_amount:
            return False, 'Not enough balance'
        
        #close loan
        loan_response = await client.patch(
            f"{URL}/rest/v1/loans",
            headers = {**HEADERS , 'Prefer': 'return=representation'},
            params ={
                'id' : f'eq.{loan_id}',
                'borrower_id' : f'eq.{borrower_id}'

            },
            json = {'status' : 'closed'}
        )
        loan_data = loan_response.json()[0]
        lender_id = loan_data['lender_id']
        print('STATUS', loan_response.status_code)
        print('BODY', loan_response.text)

        if not loan_response.json():
            return False, "Loan not found or already closed"
        # deduct user balance
        new_balance = current_balance - return_amount
        await client.patch(
            f"{URL}/rest/v1/users",
            headers  = {**HEADERS , 'Prefer' : 'return=representation'},
            params = {
                'id' : f'eq.{borrower_id}'},
            json = {'balance': new_balance}
        )
        # adding to lender 
        lender_response = await client.get(
            f'{URL}/rest/v1/users',
            headers = HEADERS ,
            params = { 'id' : f'eq.{lender_id}', 'select' : 'balance'}
        )
        print('STATUS', lender_response.status_code)
        print('BODY', lender_response.text)
        lender_balance = lender_response.json()[0]['balance']
        new_lender_balance = lender_balance + return_amount
        await client.patch(
            f'{URL}/rest/v1/users',
            headers = {**HEADERS, 'Prefer' : 'return=representation'},
            params = {'id' : f'eq.{lender_id}'},
            json = {'balance' : new_lender_balance}
        )


        return True, f'Loan repaid'
    except Exception as e:
        return False, f"Error: {str(e)}"