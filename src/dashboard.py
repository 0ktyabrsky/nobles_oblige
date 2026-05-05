import flet as ft
from servises.user_servises import get_user_by_phone
from stored.store import load_user
from Test import mobile_wrapper

from servises.sessions_services import get_pending_session
from servises.sessions_services import get_session_with_lender
from servises.sessions_services import cancel_session
from servises.sessions_services import update_session


import asyncio





def dashboard_view(page : ft.Page):

# determing all onjects in dashboard page
    # getting user's data

    user = page.data.get("User") if page.data else None
    print(user)
    saved_user = load_user()
    
    user_data =  None               
# showing invitation pop up to borrower
    async def show_invitation_popup(session):
        #taking lender's data
        full_session = await get_session_with_lender(session['id'])
        lender_name = full_session['users']['name'] if full_session else 'Someone'

        #handlers ( handle go, handle dismiss)
        async def handle_go(e):
            
            nonlocal dashboard_polling_active
            dashboard_polling_active = False
            '''

            await update_session(session['id'], 'borrower')
            page.data['session_id'] = session['id']
            print(f"User session id data stored: {page.data.get('session_id')}")

            page.data['role'] = 'borrower'
            print(f"User role data stored: {page.data.get('role')}")

            page.data['session'] = session
            print(f"User session data stored: {page.data.get('session')}")
            
            dialog.open = False
            #await page.push_route('/loan_creation')
            page.update()
            print(f'User {user.user_name} goes to the negotiation session with {lender_name}, negotioation session is stored: {page.data.get('session')}')
            '''
        async def handle_dismiss(e):
            '''
            await cancel_session(full_session['id'])
            dialog.open = False

            
            print('user dismissed invitation')
            page.update()
            '''
        # loan invitation alert dialo
        dialog =   ft.AlertDialog(
            title = ft.Text('Contract creation'),
            content = ft.Text(f'{lender_name}  sending contract agreement'),
            actions= [
                ft.TextButton('Go', on_click = handle_go),
                ft.TextButton('Dismiss' , on_click = handle_dismiss)
            ]
        )
        print('Pop up created')
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
# searchig every 5 seccond for new session created
    dashboard_polling_active = True
    async def start_polling():
        nonlocal dashboard_polling_active
        active_session_id = None # tracking active sessions id
        while dashboard_polling_active:
            try:
                # every time we update user balance
                session = await get_pending_session(user.user_id)
                print(f'dashboard pollig:Session got: {session}')
                if session and session['id'] != active_session_id:
                    active_session_id = session['id']
                    #await show_invitation_popup(session)
                    print(f'Found new loan application session')
                elif not session:
                    active_session_id = None #if not active session defining it as None
            except Exception as e:
                print(f'Polling error {e}')
            await asyncio.sleep(5)
    # endint polling when leaving
    def on_leave_dashboard():
        nonlocal dashboard_polling_active 
        dashboard_polling_active = False

    # start polling when dashboard loaded
    async def on_load():
        nonlocal user_data
        if user:
            print('polling starting')
            await start_polling()

    page.run_task(on_load)  

    async def refresh_balance():
        while dashboard_polling_active:
            user_data = await get_user_by_phone(user.user_phone)
            if user_data:
                user.balance = float(user_data['balance'])
                balance_title.value = f'{user.balance} com'
                page.update()
            await asyncio.sleep(5)


    # display user info

    # creating titles for info
    welcome_title = ft.Text(
        f"Welcome! {user.user_name}",
        size = 20,
        weight = ft.FontWeight.BOLD,
        text_align = ft.TextAlign.START
    )
    # balance
    balance_title = ft.Text(
        f'{user.balance} com',
        size = 50,
        weight = ft.FontWeight.NORMAL,
        text_align = ft.TextAlign.CENTER
    )

    

    # lend money button
    # handling pressing button
    async def handle_lend_money(e):
        print('Lend money is clicked')
        print(f'Current route {page.route}')

        # transfering to the page for money lending
        await page.push_route('/lend_money')
        print('Navigating to the lend money')

    # button itself
    
    lend_money = ft.Button(
        content = ft.Column(
            [
                ft.Icon( ft.Icons.ARROW_UPWARD, color = ft.Colors.WHITE),
                ft.Text( 'Lend', color = ft.Colors.WHITE, size = 12),
            ],
            
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        
        ),
        bgcolor= ft.Colors.GREEN,
        
        on_click = handle_lend_money,
        style = ft.ButtonStyle(
            shape = ft.RoundedRectangleBorder( radius = 50),
            padding = 20
        ))
    
    


    
    print( 'Lend money button is created')
    
    # borrow money application button

    async def handle_borrow_money(e):
        print( 'Borrow money button is clicked')
        print(f"Current route {page.route}")

        # transfering to contract creation for borrow money reuest
        welcome_title.value = 'This function will be updated in next versions'
        #await page.push_route('/borrow_money')
        print('Navigation to the money request creation page')

    # the button
    borrow_money = ft.Button(
        content = ft.Column(
            [
                ft.Icon( ft.Icons.ARROW_DOWNWARD, color = ft.Colors.WHITE),
                ft.Text( 'Borrow', color = ft.Colors.WHITE, size = 12),
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,

            
    ),
    bgcolor= ft.Colors.BLUE,
    on_click = handle_borrow_money,
    style = ft.ButtonStyle(
        shape = ft.RoundedRectangleBorder(radius = 50),
        padding = 20
    )
    )



    

    # investments list button handling
    async def handle_investment_list(e):
        print('Lend list is clicked')
        print(f'Current route {page.route}')

        # transfering user to the list of people he lended money
        await page.push_route('/investments')
        print('Navigating to the invetments list')

    # the button itself
    investments = ft.Button(
        content = ft.Text('Contracts'),
        color = ft.Colors.BLUE_300,
        on_click = handle_investment_list,

        #styling button
        style = ft.ButtonStyle(
            shape = ft.RoundedRectangleBorder(radius = 8),
            bgcolor = ft.Colors.WHITE
        )
    )
    print('Contracts button is clicked')



    # your loan list button

    # your loan list handling
    async def handle_loans(e):
        print('Loans list is clicked')
        print(f'Current route {page.route}')

        # navigating to the loan list
        await page.push_route('/loans')
        print('Navigating into loans')

    # the button itself
    loans = ft.Button(
        content = ft.Text('Loans'),
        color = ft.Colors.RED,
        on_click = handle_loans,

        #styling
        style = ft.ButtonStyle(
            shape = ft.RoundedRectangleBorder(radius = 8),
            bgcolor = ft.Colors.WHITE,
        )
    )
    async def handle_test_dashboard(e):
        nonlocal dashboard_polling_active
        print('Test dashboard is clicked')
        print(f'Current route {page.route}')

        # navigating to the loan list
        dashboard_polling_active  = False
        await page.push_route('/dashboard_2')
        print('Navigating into test dashboard') 



    test_dsh = ft.Button(
        content = ft.Text('test_dashboard'),
        color = ft.Colors.GREY,
        on_click = handle_test_dashboard,

        style = ft.ButtonStyle(
            shape = ft.RoundedRectangleBorder(radius = 8),
            bgcolor = ft.Colors.WHITE,
        )


    )

    return ft.View(
        route = '/dashboard',
        controls = [
            mobile_wrapper(
                ft.Container(
                    expand = True,
                    padding = 20, 
                    content= ft.Column(
                        expand = True,
                        alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                        controls = [


                            # top section 
                            ft.Column(
                                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                controls = [
                                    welcome_title,
                                    ft.Container(height = 10),
                                    test_dsh,
                                    ft.Container(height = 20),
                                    balance_title

                                ],   
                            ),
                            # air between sections
                            ft.Container ( height = 200),
                            # middle section
                            ft.Container(
                                padding = 20,
                                bgcolor = ft.Colors.GREY_100,
                                border_radius = 15,
                                content = ft.Column(
                                    spacing = 20,
                                    horizontal_alignment  = ft.CrossAxisAlignment.CENTER,
                                    controls = [
                                        ft.Row(
                                            alignment = ft.MainAxisAlignment.CENTER,
                                            spacing = 20,
                                            controls = [
                                                ft.Container(width = 120, content = lend_money),
                                                ft.Container(width = 120, content = borrow_money),
                                            ],

                                        ),
                                        # contracts & loans
                                        ft.Row(
                                            alignment = ft.MainAxisAlignment.CENTER,
                                            spacing = 20,
                                            controls = [
                                                ft.Container(width = 120 , content = investments),
                                                ft.Container( width  = 120, content = loans)
                                            ],
                                        ),
                                    ],

                                ),
                            ),
                            # bottom spacing
                            ft.Container(height = 10)
                        ],
                    ),
                )
            )
        ],
    )