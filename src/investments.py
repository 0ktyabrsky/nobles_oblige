import flet as ft
from Test import mobile_wrapper
import asyncio
from servises.loan_services import get_loans_by_lender

def investments_view(page : ft.Page):
# taking all user data
    user = page.data.get('User') if page.data else None
    
    contract_list_column = ft.Column(spacing = 10)


# User's states     
    margin_text = '...'
    loans_text = '...'
    expected_return_text = '...'
    total_lent_text = '...'

# handlers
    # handling back
    async def handle_back(e):
        print('Back button is clicked')
        print(f'Current route {page.route}')
        await page.push_route('/dashboard')
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
    async def show_contracts():
        contracts = await get_loans_by_lender(user.user_id)
        if not contracts:
            list_loan_notification.value = "You don't create contracts yet"
            page.update()
            return
        
        total_lent = sum( c['amount'] for c in contracts)
        
        margin = sum( c['return_amount'] for c in contracts)
        expected_return = margin * 0.8
        total_contracts = len(contracts)


        total_lent_card.content.controls[0].value = str(round(total_lent, 2))
        expected_return_card.content.controls[0].value = str(round(expected_return, 2))
        margin_card.content.controls[0].value = str(margin)
        loans_card.content.controls[0].value = str(total_contracts)

        for contract in contracts:
            borrower_name = contract['users']['name']
            row = ft.Row(
                [
                    ft.Text( borrower_name, weight ='bold'),
                    ft.Text(f"{contract['amount']} сом"),
                    ft.Text( contract['status']),
                    ft.Button('more')
                ], 
                alignment = 'spaceBetween'
            )
            contract_list_column.controls.append(row)
        
        page.update()
    page.run_task(show_contracts)
    # Contracts list's Container
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
                        contract_list_column
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