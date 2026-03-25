import flet as ft
from servises.user_servises import get_user_by_phone
from stored.store import load_user
from Test import mobile_wrapper

from servises.sessions_services import get_pending_session
from servises.sessions_services import get_session_with_lender

import asyncio
import threading





def dashboard_view(page : ft.Page):

# determing all onjects in dashboard page
    # getting user's data

    user = page.data.get("User") if page.data else None
    print(user)
    saved_user = load_user()
    
    user_data = get_user_by_phone(saved_user['user_phone'])  if saved_user else None
# showing invitation pop up to borrower
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
            print('Pop up created'),
            title = ft.Text('Contract creation'),
            content = ft.Text(f'{lender_name}  sending contract agreement'),
            actions= [
                ft.TextButton('Go', on_click = handle_go),
                print('Go button created'),
                ft.TextButton('Dismiss' , on_click = handle_dismiss),
                print('Dismiss button created')
            ]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
# searchig every 5 seccond for new session created
    def start_polling():
        def poll():
            while True:
                try:
                    session = get_pending_session(user.user_id)
                    print(f'Session got: {session}')
                    if session:
                        show_invitation_popup()
                        break
                except Exception as e:
                    print(f'Polling error {e}')
                threading.Event().wait(5)
        thread = threading.Thread(target = poll, daemon = True)
        thread.start()
    # clean up when leaving page
    def on_view_pop(e):
        print('Left dashboard')
    # start polling when dashboard loads
    if user:
        print('polling starts')
        start_polling()

    # display user info
    if user_data:
        welcome_text = f'Welcome {user.user_name}!'
        balance  = f'{user.balance} сом'
    else:
        welcome_text = 'Welcome!'
    # creating titles for info
    welcome_title = ft.Text(
        welcome_text,
        size = 20,
        weight = ft.FontWeight.BOLD,
        text_align = ft.TextAlign.START
    )
    # balance
    balance_title = ft.Text(
        balance,
        size = 50,
        weight = ft.FontWeight.NORMAL,
        text_align = ft.TextAlign.CENTER
    )

    

    # lend money button
    # handling pressing button
    def handle_lend_money(e):
        print('Lend money is clicked')
        print(f'Current route {page.route}')

        # transfering to the page for money lending
        page.go('/lend_money')
        print('Navigating to the lend money')

    # button itself
    
    lend_money = ft.ElevatedButton(
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

    def handle_borrow_money(e):
        print( 'Borrow money button is clicked')
        print(f"Current route {page.route}")

        # transfering to contract creation for borrow money reuest
        page.go('/borrow_money')
        print('Navigation to the money request creation page')

    # the button
    borrow_money = ft.ElevatedButton(
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
    def handle_investment_list(e):
        print('Lend list is clicked')
        print(f'Current route {page.route}')

        # transfering user to the list of people he lended money
        page.go('/investments')
        print('Navigating to the invetments list')

    # the button itself
    investments = ft.ElevatedButton(
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
    def handle_loans(e):
        print('Loans list is clicked')
        print(f'Current route {page.route}')

        # navigating to the loan list
        page.go('/loans')
        print('Navigating into loans')

    # the button itself
    loans = ft.ElevatedButton(
        content = ft.Text('Loans'),
        color = ft.Colors.RED,
        on_click = handle_loans,

        #styling
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