import flet as ft
from servises.user_servises import get_user_by_phone
from stored.store import load_user
from Test import mobile_wrapper

from servises.sessions_services import get_pending_session
from servises.sessions_services import get_session_with_lender
from servises.sessions_services import cancel_session
from servises.sessions_services import update_session
from servises.messanger_services import create_group, get_user_groups, get_dm_partner , get_avatar_color , get_last_message_batch,format_message_date, safe_get_dm_partner
from real_time.realtime_manager import realtime_manager
from stored.store import clear_user




import asyncio





def dashboard_2_view(page : ft.Page):

# determing all onjects in dashboard page
    # getting user's data
    
    user = page.data.get("User") if page.data else None
    user_groups = None
    group_list = ft.ListView()
    

    #making contat container for each chat
    
    
    
    async def load_data():
        nonlocal group_list
        groups = await get_user_groups(user.user_id)
        groups_ids =[ g['group_id'] for g in groups]
        last_messages = await get_last_message_batch(groups_ids)
        
        print(f'We find this group:{groups}')
        print(f'We find groups last messages: {last_messages}')

        for group in groups:
            print(f'Group for message: {group}')
            last_message = None
            last_message_date = None
            sender_name = None
            if last_messages:
                msg = last_messages.get(group['group_id'])
                print(f'This is msg: {msg}')
                if msg is not None:
                    sender_name = msg['sender_name'] if group['groups']['type'] != 'dm' else None
                    last_message = msg['content']
                    last_message_date = format_message_date(msg['sent_at'])
                
            group_list.controls.append(
                await build_group_tile(group, user.user_id, last_message , last_message_date, sender_name)
                )
        

        page.update()
    # handlig log out button
    async def handle_log_out(e):
        print('Log out is clicked')
        print(f'Current route {page.route}')
    
        clear_user()
        await page.push_route('/login')
        print('Navigating to the log in')

    async def build_group_tile(group, current_user_id: str , last_message, last_message_date, sender_name):
        partner_initials = '?'
        display_name = None
        display_id = None
        if group['groups']['type'] == 'dm':
            partner =  await safe_get_dm_partner(group['group_id'], current_user_id)
            print(f'Dm partner: {partner}')
            if not partner:            
                display_name= 'Loading..'
                partner_initials = '?'
                subtitle_text = last_message or ''
            else:
                display_name= partner['users']['name']
                display_id = partner['user_id']
                print(f'Displayed name: {display_name}')
                subtitle_text = last_message or ""
                partner_initials =  display_name[:1].capitalize()
        else:
            display_name = group['groups']['name']
            subtitle_text = f'{sender_name}:{last_message}' or ''
            partner_initials = display_name[:1].capitalize()
        
        chat = ft.ListTile(
            data = group['group_id'],
            title = ft.Text(display_name, size = 18 , weight = ft.FontWeight.BOLD),
            subtitle = ft.Text(subtitle_text or '', size = 10),
            trailing = ft.Text(last_message_date or ''), # must be column so i can add an indicator at the bottom to notify user for new messages , lendings etc

            leading = ft.CircleAvatar(
                content = ft.Text(partner_initials),
                color = ft.Colors.WHITE,
                bgcolor = get_avatar_color(display_name)
            ))
        chat.on_click = lambda e, group = group , dm_name = display_name, dm_id = display_id : handle_click_chat( e , group, dm_name,dm_id )
        return chat
    def handle_click_chat( e , group, dm_name, dm_id = None):
        
        print(f'This is grop user clicked: {group}')
        if group['groups']['type'] == 'dm':
            page.data['dm_companion'] = {}
        page.data['current_group'] = {
            **group,
            'display_name' : dm_name,
            'display_id' :dm_id if dm_id else 'No id to display'
        }
        page.run_task(page.push_route, '/chat')

        print('the tile i clicked')
    async def on_new_group(record):
        print(f'New group realtime: {record}')

        group_id = record['group_id']

        groups = await get_user_groups(user.user_id)

        group = next((g for g in groups if g['group_id'] == group_id),None)

        if not group:
            return
        
        last_messages = await get_last_message_batch([group_id])
        msg=  last_messages.get(group_id) if last_messages else None

        sender_name = None
        if msg and group['groups']['type'] != 'dm':
            sender_name = msg['sender_name']
        
        last_message  = msg['content'] if msg else None
        last_message_date = format_message_date(msg['sent_at'] if msg else None)

        tile = await build_group_tile(
            group,
            user.user_id,
            last_message,
            last_message_date,
            sender_name
        )
        print(
            'tile created, updating page'
        )
       
        group_list.controls.append(tile)

        page.update()
        #group_list.controls.append(await build_group_tile())

    async def on_delete_group(record):
        print('on delete triggered' , record)
        # getting deleted group_id
        group_id = record['group_id']

        group_list.controls = [
            tile for tile in group_list.controls
            if tile.data != group_id
        ]
        page.update()
        print('After deleting group updating page')
    

    async def on_new_message(record):
        group_id = record['group_id']
        new_content = record['content']
        sent_at = record['sent_at']

        target_tile = None
        for control in group_list.controls:
            if control.data == group_id:
                target_tile = control
                break
        if target_tile:
            target_tile.subtitle.value = new_content

            if sent_at:
                target_tile.trailing.value = format_message_date(sent_at)
                

            group_list.controls.remove(target_tile)
            group_list.controls.insert(0, target_tile)


            group_list.update()
        else:
            print('"CHat not found')
    
        



    # adding realtime listening
    realtime_manager.on_new_group = on_new_group
    realtime_manager.on_delete_group = on_delete_group
    realtime_manager.on_new_message = on_new_message
    

    
    user_data =  None               
# showing invitation pop up to borrower
    


    # display user info

    # creating titles for info
    welcome_title = ft.Text(
        "Konnekt",
        size = 20,
        weight = ft.FontWeight.BOLD,
        text_align = ft.TextAlign.START
    )
    # balance
    balance_title = ft.Text(
        f'{user.balance} com',
        size = 15,
        weight = ft.FontWeight.NORMAL,
        text_align = ft.TextAlign.CENTER
    )
    # search bar field: text field + buton (searching for messages)
    search_bar = ft.Container(
        content =  ft.TextField(
            hint_text = 'Search',
            prefix_icon = ft.Icons.SEARCH,
            text_size = 15,
            border = ft.InputBorder.NONE,
            content_padding=  ft.Padding.only(left = 15, right = 15, bottom = 15),
        ),
        bgcolor = ft.Colors.GREY_200,
        border_radius = 30,
        height = 35,
        padding = 0
        )
    log_out_button = ft.IconButton(
        icon = ft.Icons.LOGOUT,
        on_click = handle_log_out
    )

    # cloud buttons with taggs (filetring chats)


    # profile icon button (setting)

    # overlay add new chat button
    new_group = ft.FloatingActionButton(
        icon = ft.Icons.CHAT_ROUNDED,
        on_click = None,
        bgcolor = ft.Colors.BLUE_200,
        align = ft.Alignment.BOTTOM_RIGHT
    )

    # navogation bar
    


    async def on_nav_change(e):
        index = e.control.selected_index
        print(f' nav_bar selected index: {index}')
        routes = ['/dashboard_2' , '/dashboard' ,'/dashboard', '/dashboard', '/dashboard']
        target = routes[index]
        if page.route == target:
            return
        await page.push_route(target)

    
            
    

    page.run_task(load_data)
    page.run_task(realtime_manager.connect_groups,user.user_id)
    #page.run_task(realtime_manager.connect_messages, grp_id)
    print(F"CURRENT contacts: {group_list.controls}")
    return ft.View(
        route = '/dashboard_2',
        controls= [
            mobile_wrapper(
                ft.Column(
                    expand = True,
                    spacing = 0,
                    height  = page.height,
                    controls = [
                        ft.Container(
                        expand = True,
                        padding = 20,
                        content = ft.Column(
                            expand = True,
                            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                            controls = [
                                ft.Row(
                                    controls = [ welcome_title , balance_title, log_out_button],
                                    spacing= 30,
                                    tight= True,
                                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment= ft.CrossAxisAlignment.CENTER
                                ),
                             search_bar,
                             ft.Container(expand = True, content= group_list)
                         ]
                     )
                ),
                new_group,
                ft.Container(height = 10),
                ft.NavigationBar(
                    destinations=[
                        ft.NavigationBarDestination(icon=ft.Icons.CHAT,    label='Chat'),
                        ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label='Updates'),
                        ft.NavigationBarDestination(icon=ft.Icons.QR_CODE),
                        ft.NavigationBarDestination(icon=ft.Icons.GROUPS,  label='Community'),
                        ft.NavigationBarDestination(icon=ft.Icons.CALL,    label='Calls'),

                ],
                on_change = on_nav_change
                )  
            ]
            )
        )
        ]
    )
