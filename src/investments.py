import flet as ft
from Test import mobile_wrapper

def investments_view(page : ft.Page):
# taking all user data
    user = page.data.get('User') if page.data else None
    user_info = user.info()
    user_contracts = user.given_loans


# User's states     
    margin_text = f'{user_info['Margin']}'
    loans_text = f'{user_info['TotalContracts']}'
    expected_return_text = f'{user_info['ExpectedReturn']}'
    total_lent_text = f'{user_info['Total_lent']}'

# handlers
    # handling back
    def handle_back(e):
        print('Back button is clicked')
        print(f'Current route {page.route}')
        page.go('/dashboard')
        print("Navigating to dashboard")

    # hadling loan details
# header 
    # back button 
    back_button = ft.IconButton(
        icon = ft.Icons.ARROW_BACK,
        icon_size = 24,
        on_click = handle_back,

        tooltip = 'Back to Dashboard',
        icon_color = ft.Colors.GREY_800
    )
    

# card titles

    main_title = ft.Text(
        'Portfolio',
        size = 32,
        weight = ft.FontWeight.BOLD,
        text_align = ft.TextAlign.CENTER,
        color = ft.Colors.GREY_800

    )
    print('main title is created')
    # total lent
    total_lent_card = ft.Container(
        content = ft.Column(
            controls= [
                ft.Text(
                    total_lent_text,
                    size = 40,
                    weight = ft.FontWeight.BOLD,
                    color= ft.Colors.BLACK
                ),
                ft.Text(
                    "Total lent сом",
                    size = 16,
                    weight = ft.FontWeight.W_500
                ),
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 0,
        ),
        bgcolor = ft.Colors.WHITE,
        padding = 20,
        border_radius = 25,
        expand= True
    )
    
    # Total expected return
    expected_return_card = ft.Container(
        content = ft.Column(
            [
                ft.Text(expected_return_text, size = 35, weight =ft.FontWeight.BOLD, color = ft.Colors.GREEN_400),
                ft.Text( 'Return сом' , size = 16 , color = ft.Colors.GREEN_400)
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 0,
        ),
        bgcolor = ft.Colors.WHITE,
        padding = 20,
        border_radius = 25,
        expand= True
    )
    # Total marging 
    margin_card = ft.Container(
        content = ft.Column(
            [
                ft.Text(margin_text, size = 35, weight =ft.FontWeight.BOLD, color = ft.Colors.GREEN_400),
                ft.Text( 'Margin сом' , size = 16 , color = ft.Colors.GREEN_400)
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 0,
        ),
        bgcolor = ft.Colors.WHITE,
        padding = 20,
        border_radius = 25,
        expand= True
    )
    # total loan number
    loans_card = ft.Container(
        content = ft.Column(
            [
                ft.Text(loans_text, size = 35, weight =ft.FontWeight.BOLD, color = ft.Colors.BLACK),
                ft.Text( 'Loans' , size = 16 , color = ft.Colors.BLACK)
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 0,
        ),
        bgcolor = ft.Colors.WHITE,
        padding = 20,
        border_radius = 25,
        expand= True
    )


# header container
    header = ft.Container(
        content = ft.Row(
            [
                back_button,
                main_title
            ],
            alignment = ft.MainAxisAlignment.START,
            spacing = 8
            
        ),
        padding = ft.Padding.only( left = 8 ,top = 16, right = 16, bottom = 8)
    )
# User stats 
    stats_container = ft.Column(
        spacing = 10,
        controls = [

            ft.Row(controls= [expected_return_card,margin_card ],alignment = ft.MainAxisAlignment.CENTER,spacing = 10),
            ft.Row( controls = [total_lent_card , loans_card], alignment = ft.MainAxisAlignment.CENTER,spacing = 10),

        ]
)
# list of current lended loans
    list_loan_title = ft.Text(
        "Contracts",
        size = 20, 
        weight = ft.FontWeight.BOLD,
        text_align = ft.TextAlign.START
    )
    # for any problem with contract's list
    list_loan_notification = ft.Text(
        '',
        weight = ft.FontWeight.BOLD,
        text_align = ft.TextAlign.START)
    
    # loading loan information
    def show_contracts(user_contracts):
        contract_rows = []
        if user_contracts:
            for contract in user_contracts:
                data = contract.lender_view()
                # creating a container for each loan
                row = ft.Row(
                    [
                        ft.Text( data['Borrower'], weight ='bold'),
                        ft.Text(f"{data['AmountLent']} сом"),
                        ft.Text( data['Status']),
                        ft.ElevatedButton('more')
                    ], alignment = 'spaceBetween'
                )
                contract_rows.append(row)

        else:
            list_loan_notification.value = "You don't create contracts yet"
        return contract_rows
    # Contracts list's Container
    contract_list = ft.Column(
        controls = show_contracts(user_contracts),
        spacing = 10
    )
    # main container
    

    return ft.View(
        route = '/investments',
        controls = [
            mobile_wrapper(
                ft.Column(
                    spacing = 16,
                    controls= [
                        header,
                        stats_container,
                        list_loan_title,
                        list_loan_notification,
                        contract_list
                    ]
                )
            )
        ]
    )

# here is the place where all your 
"""
        plan for page
    a generative list of credits

    header(
        Back button | Main title (Investments)

        Title "total investments ( takes value from all loans )
        Total expected return from all investments ( takes value from all loans)
    )
    title "loans"
    each row contain basic loan info: 
        Borrower
        Loan amount ,
        loan term,
        Total debt,
        your margin,
        button 'Details' -show all information about loan


        




"""