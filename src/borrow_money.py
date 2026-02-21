import flet as ft
from Test import mobile_wrapper

# User search another user to lend him money via phone number

def borrow_money_view(page: ft.Page):

    # handling search borrower button
    def handle_search(e):

        print('Search is clicked')
        print(f'Current route {page.route}')

        # getting phone number to search in Data Base
        phone = creditor_phonenumber.value
        print("Borrowers phone number is got")

        # here we search thise phone number in BD and if it doesnt find it, show error



        # if found successfuly go the the loan agreement page
        page.go('/loan_request')
        print('Navigated to the loan request page')
    
    title= ft.Text( # explanation text " Find by phone number"
        'Find by phone number' ,
         size = 40,
         weight = ft.FontWeight.NORMAL,
         text_align = ft.TextAlign.CENTER
        )
    print('title created')

    creditor_phonenumber = ft.TextField( # user search borrower's account by phone number 
        label = 'Phone number +996',
        width = 300
        # only numeric value
    )
    print('Search creditor by phone number from created')
    
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
            [title,
             creditor_phonenumber,
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
        route = '/borrow_money',
        controls = [
            mobile_wrapper(
                ft.Column(
                    spacing = 16,
                    controls = [
                        ft.Container ( height = 20),
                        main_container
                    ],
                    horizontal_alignment= ft.CrossAxisAlignment.CENTER

                )
            )
        ]
    )