import flet as ft
from Test import mobile_wrapper

from stored.store import load_user


from servises.user_servises import get_user_by_phone
from servises.sessions_services import (create_session, get_pending_session)



# User search another user to lend him money via phone number

def lend_money_view(page: ft.Page):
    # user data 
    user = page.data.get('User') if page.data else None
    saved_user = load_user()

    # handling back button
    def handle_back(e):
        print('back button is clicked')
        print(f'Current route {page.route}')
        page.go('/dashboard')
        print('Navigated to dashboard')
    # handling search borrower button
    async def handle_search(e):

        print('Search is clicked')
        print(f'Current route {page.route}')
        # disablenig button until result is sent
        search.disabled = True
        search.bgcolor = ft.Colors.GREY_400
        page.update()

        # getting phone number to search in Data Base
        phone = borrower_phonenumber.value
        print(f"Borrowers phone number is got {phone}")
        try:
            #searching that borrower in DataBase
            borrower = await get_user_by_phone(phone)
            
            print(f'From db borrower info: {borrower}')
        except Exception:
            
            title.value = 'Network Error'
            title.color = ft.Colors.RED_400
            search.disabled = False
            page.update()
            return
        

        if not borrower:
            title.value = 'User not found.'
            title.color = ft.Colors.RED_400
            page.update()
            return 
        
        if borrower['id'] == user.user_id:
            print('Borrower id and lender id the same, must be different')
            title.value = "You can't lend yourself"
            title.color = ft.Colors.RED_400
            page.update()      

        try:
            pending_session = await get_pending_session(borrower['id'])
        except Exception:
            title.value = 'Network Error'
            title.color = ft.Colors.RED_400
            search.disabled = False
            page.update()
            return

        if pending_session and pending_session['status'] == 'pending':
            print("You can't create an active session with this user, it already in session with someone")
            title.value = f"{borrower['name']} have active session, try later"
            title.color = ft.Colors.RED_400
            page.update()
            return
        
        try:
            negotiation_session = await create_session(lender_id = user.user_id
                                                        , borrower_id = borrower['id'],
                                                          role = 'lender'
                                                          )
        except Exception:
                title.value = 'Failed to create session. Try again'
                title.color= ft.Colors.RED_400
                page.update()
                return
        
        # if found successfuly go the the loan agreement page
        print(f'session_ created {negotiation_session}')
        # storing inforation to pass it to another page

        page.data['session'] = negotiation_session
        print(f"Lender session data stored: {page.data.get('session')}")

        page.data['session_id'] = negotiation_session['id']
        print(f"Lender session id data stored: {page.data.get('session_id')}")

        page.data['role'] = 'lender'
        print(f"User role data stored: {page.data.get('role')}")

        await page.push_route('/loan_creation')
        print('navigating to loan creation form')

    


    
    title= ft.Text( # explanation text " Find by phone number"
        'Find by phone number' ,
         size = 24,
         weight = ft.FontWeight.NORMAL,
         text_align = ft.TextAlign.CENTER
        )
    print('title created')

    borrower_phonenumber = ft.TextField( # user search borrower's account by phone number 
        label = 'Phone number +996',
        width = 300
        # only numeric value
    )
    print('Search borrower by phone number from created')
    back_button = ft.IconButton(
        ft.Icons.ARROW_BACK,
        icon_size = 24,
        on_click = handle_back,

        tooltip = 'Back to Dashboard',
        icon_color = ft.Colors.GREY_800
    )
    # search button
    search = ft.ElevatedButton(
        content = ft.Text('Search'),
        color = ft.Colors.WHITE,
        on_click = handle_search,
        #  check data for any issue
        # transfer user tp the loan creation page

        # button style
        style = ft.ButtonStyle(
            shape = ft.RoundedRectangleBorder(radius = 8),
            bgcolor = ft.Colors.AMBER
        )
    )
    print('Search borrower button created')
    

    # main container for phone number text field and search button

    main_container = ft.Container(
        content = ft.Column(
            
            [ft.Row(controls = [
                back_button , title,
            ]
            ),
             borrower_phonenumber,
             search],

            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 10
        ),
        padding = 20,
        border_radius = 10,
        bgcolor =ft.Colors.WHITE,
        width = 500,
        shadow = ft.BoxShadow(
            spread_radius = 1,
            blur_radius = 15,
            color = ft.Colors.BLACK_12,
            offset = ft.Offset( 0 , 2)
        )
    )
    # showing this page to the user
    return ft.View(
        route = '/lend_money',
        controls = [
            mobile_wrapper(
                ft.Column(
                    spacing = 16,
                    controls = [

                        ft.Container ( height = 60),
                        main_container
                    ],
                    horizontal_alignment= ft.CrossAxisAlignment.CENTER

                )
            )
        ]
    )