from db import HEADERS, URL
import httpx
client = httpx.AsyncClient()
import flet as ft
from datetime import datetime , timezone
import time
import asyncio


async def create_group(created_by: str , group_type : str,name: str = None, members_ids: list = None ):
    members_ids = members_ids or []
    response = await client.post(
        f"{URL}/rest/v1/groups",
        headers = {**HEADERS, 'Prefer': 'return=representation'},
        json = {
            'name': name,
            'type' : group_type,
            'created_by' : created_by
        }
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)

    group = response.json()[0]

    # adding members to the group
    members = [{'group_id' : group['id'], 'user_id': created_by , 'role': 'admin' if group_type == 'group' else 'member'}]
    for user_id in members_ids:
        members.append({'group_id': group['id'], 'user_id': user_id, 'role': 'member'})

    # call to supabase table
    await add_members(group['id'], members)
    return group




async def add_members(group_id , members: list = None ):
    members = members or []

    response = await client.post(
        f"{URL}/rest/v1/group_members",
        headers = HEADERS,
        json = members
    )
    print('STATUS', response.status_code)
    print('BODY', response.text)
    return response.json()

# getting exsisting groups
async def get_user_groups(user_id):
    response = await client.get(
        f"{URL}/rest/v1/group_members",
        headers = HEADERS,
        params = {
            'user_id': f'eq.{user_id}',
            'select': '*, groups(id, name, type)'

        }
    )
    print('get user_groups STATUS', response.status_code)
    print('BODY', response.text)
    return response.json() or []
# how to get last message inside each group??
async def get_last_message_batch(group_id: str):
    response = await client.post(
        f'{URL}/rest/v1/rpc/get_last_message_for_groups',
        headers  = HEADERS,
        json = { 'groups_ids' : group_id
        }

    )
    print('get last messages STATUS', response.status_code)
    print('BODY', response.text)
    messages = response.json() or []
    return {msg['group_id']: msg for msg in messages}

def format_message_date(timestamp: str):
    if not timestamp:
        return ''
    dt = datetime.fromisoformat(timestamp)
    local_dt = dt.astimezone()
    return local_dt.strftime('%H:%M')

async def get_dm_partner(group_id: str, current_user_id: str):
    response = await client.get(
        f"{URL}/rest/v1/group_members",
        headers = HEADERS,
        params = {
            'group_id' : f'eq.{group_id}',
            'user_id': f"neq.{current_user_id}",
            'select' : 'user_id, users(name)'
        }

    )
    print('get_dm_STATUS', response.status_code)
    print('get_dm_BODY', response.text)
    data = response.json()
    return data[0] if data else None

def get_avatar_color(user_name: str):
    colors_lookup = [
            ft.Colors.AMBER,
            ft.Colors.BLUE,
            ft.Colors.BROWN,
            ft.Colors.CYAN,
            ft.Colors.GREEN,
            ft.Colors.INDIGO,
            ft.Colors.LIME,
            ft.Colors.ORANGE,
            ft.Colors.PINK,
            ft.Colors.PURPLE,
            ft.Colors.RED,
            ft.Colors.TEAL,
            ft.Colors.YELLOW
        ]
    return colors_lookup[hash(user_name)% len(colors_lookup)]

async def safe_get_dm_partner(group_id, user_id):
    for _ in range(5):
        partner = await get_dm_partner(group_id, user_id)
        print('get_safe_dm_STATUS', partner)
        
        if partner:
            return partner
        await asyncio.sleep(1)
    return None
