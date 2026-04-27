import flet as ft
from servises import user as us

# windows screen settings 
MOBILE_WIDTH = 380
def mobile_wrapper(content):
    return ft.Row(
        alignment = ft.MainAxisAlignment.CENTER,
        expand = True,
        controls= [
            ft.Container(
                width = MOBILE_WIDTH,
                padding = 16,
                content = content
            )
        ]
    )


test_user = us.User('9942', 'Simba', '996707143170', balance = 1000)


'''
# negotiation sessions notification popup
    def show_invitation_popup(session):
        #taking lender's data
        full_session = get_session_with_lender(session['id'])
        lender_name = full_session['users']['name'] if full_session else 'Someone'

        #handlers ( handle go, handle dismiss)
        def handle_go(e):
            page.data['session_id'] = session['id']
            dialog.open = False
            page.update()
            print('The user is in the loan negotiation') # here i add negotiation session page

        def handle_dismiss(e):
            dialog.open = False
            print('user dismissed invitation')
            page.update()
        # loan invitation alert dialo
        dialog =   ft.AlertDialog(
            title = ft.Text('Contract creation'),
            content = ft.Text(f'{lender_name}  sending contract agreement'),
            actions= [
                ft.TextButton('Go', on_click = handle_go),
                ft.TextButton('Dismiss' , on_click = handle_dismiss)
            ]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
    # realtime negotiation listener
    def start_realtime():
        # triger if new session creatid in session table
        async def listen():
            async_supabase = await get_async_client()
            
            def handle_insert(payload):
                print( f'New session is recieved {payload}')
                new_session = payload['record']
                # cheking if it a session where user is borrower and show him popup message
                if str(new_session['borrower_id']) ==  str(user.user_id):
                    show_invitation_popup(new_session)
                
            # chanel for sessions
            channel = async_supabase.channel('sessions_channel')
            channel.on_postgres_changes(
                event = 'INSERT',
                schema = 'public',
                table = 'sessions',
                callback = handle_insert
            ).subscribe()
            while True:
                await asyncio.sleep(1)
        
        def run_async():
            asyncio.run(listen())

        
        
        # startin realtime channel
        def start_realtime():
            thread =threading.Thread( target = run_async ,daemon = True )
            thread.start()
        # cleaning up when leaving page
        
            
    start_realtime()

'''