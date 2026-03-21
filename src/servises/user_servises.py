'''
This file for user information administration servises
'''

'''
from db import supabase


def get_user_by_phone(phone):

    response = supabase.table("users") \
        .select("*") \
        .eq("phone", phone) \   
        .execute()

    if response.data:
        return response.data[0]

    return None


def create_user(name, phone):

    data = {
        "user_name": name,
        "phone": phone
    }

    response = supabase.table("users") \
        .insert(data) \
        .execute()

    return response.data[0]
'''
from db import supabase

def get_user_by_phone(phone):
    response = supabase.table("users")\
        .select('*')\
        .eq('phone_number' , phone)\
        .execute()
    if response.data:
        return response.data[0]
    return None

def create_user(name, phone):
    data = {
        'name' : name,
        'phone_number' : phone
    }
    response = supabase.table('users')\
    .insert(data)\
    .execute()

    return response.data[0]

# gettin user info from db otherwise creating it in db
def get_or_create_user(name, phone):
    record = get_user_by_phone(phone)
    if not record:
        record = create_user(name, phone)
    return record

