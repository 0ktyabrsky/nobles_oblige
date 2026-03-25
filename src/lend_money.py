import flet as ft
from Test import mobile_wrapper

from stored.store import load_user


from servises.user_servises import get_user_by_phone
from servises.sessions_services import create_session

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
    def handle_search(e):

        print('Search is clicked')
        print(f'Current route {page.route}')

        # getting phone number to search in Data Base
        phone = borrower_phonenumber.value
        print("Borrowers phone number is got")
        #searching that borrower in DataBase
        borrower = get_user_by_phone(phone)
        if borrower:
            if borrower['id'] == user.user_id:
                print('Borrower id and lender id the same, must be different')
                title.value = "You can't lend yourself"
                title.color = ft.Colors.RED_400
                page.update()
            else:
                print(f'borrower founed: {borrower}')
                negotiation_session = create_session(lender_id = user.user_id , borrower_id = borrower['id'])
                print(f'session_ created {negotiation_session}')
                page.go('/loan_creation')
                print('navigating to loan creation form')
        else:
            title.value = 'User not found.'
            title.color = ft.Colors.RED_400
            page.update()


        # here we search thise phone number in BD and if it doesnt find it, show error



        # if found successfuly go the the loan agreement page
    
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