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
    return response.jsom()[0]