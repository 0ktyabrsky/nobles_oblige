'''
here is a back end description for creating negotiation session
functions (
create session
update negotiation details
complete session
cancel session
)


'''

from db import supabase

def create_session(lender_id, borrower_id):
    data = {
        'lender_id' : lender_id,
        'borrower_id' : borrower_id,
        'status' : 'pending'
    }
    response = supabase.table('sessions')\
    .insert(data)\
    .execute()

    return response.data[0]

def update_negotiation_details(loan_amount, days, loan_due_date, return_amount):
    data = {
        'amount' :loan_amount,
        'days' : days,
        'return' : return_amount,
        'due_date' : loan_due_date
    }
    response = supabase.table('sessions')\
        .update(data)\
        .eq('id', 'session_id')\
        .execute()
    return response.data[0] 

def complete_session(session_id):
    response = supabase.table('sessions')\
        .update({'status' : 'complete'})\
        .eq('id', session_id)\
        .execute()
    return response.data[0]

def cancel_session(session_id):
    response = supabase.table('sessions')\
        .update({"status": 'cancelled'})\
        .eq('id', session_id)\
        .execute()
    return response.data[0]
def get_pending_session(borrower_id):
    response = supabase.table('sessions')\
        .select('*')\
        .eq('borrower_id', borrower_id)\
        .eq('status' , 'pending')\
        .execute()
    if response.data:
        return response.data[0]
    return None

def get_session_with_lender (session_id):
    response = supabase.table('sessions')\
        .select('*, users!lender_id(name)')\
        .eq('id', session_id)\
        .execute()
    if response.data:
        return response.data[0]
    return None