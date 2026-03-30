
import flet as ft
from Test import mobile_wrapper
import asyncio
from servises.loan_services import get_loans_by_borrower


def loans_view(page : ft.Page):
# taking all user data
    user = page.data.get('User') if page.data else None
    
    loan_list_column = ft.Column(spacing = 10)
# User's states     
    interest_text = '0'
    loans_text = '0'
    total_debt_text = '0'


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
        'Loans',
        size = 32,
        weight = ft.FontWeight.BOLD,
        text_align = ft.TextAlign.CENTER,
        color = ft.Colors.GREY_800

    )
    print('main title is created')
    # total lent
    total_debt_card = ft.Container(
        content = ft.Column(
            controls= [
                ft.Text(
                    total_debt_text,
                    size = 40,
                    weight = ft.FontWeight.BOLD,
                    color= ft.Colors.BLACK
                ),
                ft.Text(
                    "Total debt сом",
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
    
   
    # Total marging 
    interest_card = ft.Container(
        content = ft.Column(
            [
                ft.Text(interest_text, size = 35, weight =ft.FontWeight.BOLD, color = ft.Colors.RED_400),
                ft.Text( 'Interest сом' , size = 16 , color = ft.Colors.RED_400)
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

            ft.Row( controls = [total_debt_card] , alignment = ft.MainAxisAlignment.CENTER),
            ft.Row( controls = [ interest_card, loans_card], alignment = ft.MainAxisAlignment.CENTER,spacing = 10),

        ]
)
# list of current lended loans
    list_loan_title = ft.Text(
        "Loans",
        size = 20, 
        weight = ft.FontWeight.BOLD,
        text_align = ft.TextAlign.START
    )
    # for any problem with contract's list
    list_loan_notification = ft.Text(
        '',
        weight = ft.FontWeight.BOLD,
        text_align = ft.TextAlign.START)

    #loan status text 
    loan_status_text = ft.Text('', )
    # Contracts list's Container
    
    # repay button handler 
    def handle_repay(e , captured_loan , btn, status):
            print('repay loan is clicked')
            result = user.repay_debt( captured_loan.payment_amount , captured_loan.loan_id)
            print('repay loan function started')
            print(f'result {result}')
            if 'successfully' in result:                    
                
                # updating all user's data
                btn.disabled = True
                btn.bgcolor = ft.Colors.GREY_400
                btn.content = ft.Text('repayed', color = ft.Colors.WHITE)
                status.value ='closed'
                btn.update()
                
                print(' repay button is disables')
                updated_info = user.info()
                # update text values inside cards
                print(f'taking updated information {updated_info}')
                
                total_debt_card.content.controls[0].value  = f"{updated_info['TotalDebt']}"
                print(total_debt_card.content.controls[0])
                interest_card.content.controls[0].value =f"{updated_info['TotalInterest']}"
                print(interest_card.content.controls[0])
                loans_card.content.controls[0].value = f"{updated_info['LoanNumber']}"
                print(loans_card.content.controls[0])
                print('updating text in user stats cards')
                # updated loan list notification
                list_loan_notification.value = result
                list_loan_notification.color = ft.Colors.GREEN
                print('updating loan notification')
                # update page
                
                print('updating all page')
               
                page.update()
                


                
            else:
                list_loan_notification.value = result
                list_loan_notification.color = ft.Colors.RED
                list_loan_notification.update()
    
    
    # loading loan information
    async def show_loans():
        loans = await get_loans_by_borrower(user.user_id)
        if not loans:
            list_loan_notification.value = list_loan_notification.value = "You don't have loans"
            page.update()
            return
        total_debt = 0
        total_interest = 0

        
        for loan in loans:
            lender_name = loan['users']['name']
            amount = float(loan['amount'])
            return_amount = float(loan['return_amount'])
            interest = return_amount - amount
            total_debt +=return_amount
            total_interest += interest

            
            is_repayed = loan['status'] == 'closed'
            
            loan_status = ft.Text(loan['status'])
            print(is_repayed)
            
            # creating each button for each loan
            repay_button = ft.ElevatedButton(
                content = ft.Text( 'repayed' if is_repayed else 'repay', color = ft.Colors.WHITE),
                bgcolor = ft.Colors.GREY_400 if is_repayed else ft.Colors.GREEN,
                disabled = is_repayed
                
            )
            
            repay_button.on_click = lambda e , captured_loan = loan , btn = repay_button, status = loan_status: handle_repay(e , captured_loan , btn , status)

            # creating a container for each loan
            row = ft.Row(
                [
                    ft.Text( lender_name, weight ='bold'),
                    ft.Text(f"{amount} сом"),
                    loan_status,
                    repay_button
                ], alignment = 'spaceBetween'
            )
            loan_list_column.controls.append(row)
        
        total_debt_card.content.controls[0].value = str(round(total_debt, 2))
        interest_card.content.controls[0].value = str(round(total_interest, 2))
        loans_card.content.controls[0].value = str(len(loans))
        page.update()
    page.run_task(show_loans)
        
 
    
                
    
    # main container
    

    return ft.View(
        route = '/loans',
        controls = [
            mobile_wrapper(
                ft.Column(
                    spacing = 16,
                    controls= [
                        header,
                        stats_container,
                        list_loan_title,
                        list_loan_notification,
                        loan_list_column
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