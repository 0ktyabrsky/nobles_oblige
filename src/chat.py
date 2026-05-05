'''
                    Plan for this page
chat name =  companion name if group type == dm else group name
chat avatar profile = circle 
back button ,
group settings ( three vertical dots)
chat balance = group_balance if group_type == group
[back button    row(chat name, chat avatar)     chat balance     group settings]


pinned messages ( for loan agreements or polls)
[   pin image       message content]


message list scroller
    message 
    [user avatar user name      message content     sent time] if text
    [user avatar user name      loan request title, 
                                loan details 
                                agree   disagree                        
                                                    sent time           ]

send money-buble button
lend money-buble button
request money-buble button

[message input          send button]

lend 

'''

from Test import mobile_wrapper
import flet as ft
from real_time import realtime_manager
from servises.messanger_services import get_messages , get_avatar_color , send_message, format_message_date
from real_time.realtime_manager import realtime_manager

from servises.chat_engine import Message , ChatMessage , Chat




def chat_view(page: ft.Page):
    current_chat = page.data.get('current_group')
    print(f'THis is current group: {current_chat}')
    user = page.data.get('User')


    chat = Chat(page, user)

    realtime_manager.on_new_message  = chat.append_message


    async def handle_back(e):
        print('Back button is clicked')
        print(f'Current route {page.route}')
        await page.push_route('/dashboard_2')
        print("Navigating to dashboard")

    async def handle_send_message(e):
        await chat.send_message(e)

    




    back_button = ft.IconButton(
        icon = ft.Icons.ARROW_BACK,
        icon_size = 24,
        on_click = handle_back,

        tooltip = 'Back to Dashboard',
        icon_color = ft.Colors.GREY_800
    )
    chat.back_button = back_button

# where all messages will be stack
    message_input = ft.TextField(
        hint_text  ='Type a message...',
        expand = True,
        border_radius = 20,
        autofocus = True,
        min_lines = 1,
        max_lines = 5,
        filled = True
    
    )

    

    
    page.run_task(realtime_manager.connect_messages , current_chat['group_id'])
    return chat.build()
