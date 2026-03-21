import flet as ft
import datetime

from Test import mobile_wrapper
from Test import test_user


def loan_creation_view(page : ft.Page): 

    # get user's data

    user = page.data.get('User') if page.data else None
    # get date time from date picker
    today = datetime.datetime.now()
    due_date = None

# event after back to dashboard button clicked
    def handle_back(e):
        print('back button is clicked')
        print(f'Current route{page.route}')

        page.go('/dashboard')
        print('Navigatet to dashboard')
    
    
# event after send agreement click
    def handle_send_agreement(e):

    # debugging
        print('send agreement is clicked')
        print(f'Current route {page.route}')
    
        # borrower = borrower.user_name
        borrower = 'Chikitita'
        P0 = int(loan_amount.value)
        N = int(term.value)
        P = int(repay.value)

        
    # create a loan and take change balance

        result = user.lend_money_short(
            amount = P0,
            term = N,
            repay = P,
            debtor = test_user,
            loan_created_date = today.strftime('%d %m %Y'),
            loan_due_date = due_date.strftime('%d %m %Y'))
        print('Balance changed and money lended')
    # showing that loan is created
        notification_title.value = result
        # change color dependong on success
        if 'succesfully' in result.lower():

            notification_title.color = ft.Colors.GREEN_400
        else:
            notification_title.color = ft.Colors.RED_400
        page.update()

        # getting back to the dashboard
        

# all titles and buttons and fields 
    main_title = ft.Text(
        'Create a Loan',
        size = 32,
        weight = ft.FontWeight.BOLD,
        text_align = ft.TextAlign.CENTER,
        color = ft.Colors.GREY_800
    )
    print('title is created')
    
    notification_title = ft.Text( # will show if loan created or not
        '',
        size = 40,
        weight = ft.FontWeight.NORMAL,
        text_align = ft.TextAlign.CENTER

    )
    print('notification title is created')

# all fields
    # loan amount field
    loan_amount = ft.TextField(
        label = '',
        width = 300
    )

    print('Loan amount form is created')
    # loan term days
    # forms handler
    def on_form_change(e):
        nonlocal due_date
        value = e.control.value
        term_title.value = f"Loan term days: {value}"
        due_date = datetime.datetime.now() + datetime.timedelta(days = int(value))
        print(f'calculated due date: {due_date}')
        # calculate due_date by input days
        
        page.update()
    
    term = ft.TextField(
        label = '',
        width = 100,
        on_change = on_form_change
    )

    print('input loan term form is created')

    repay = ft.TextField(
        label = '',
        width = 300
    )
    print('repay form is created')
    #date piker
    
    
    #date picker handlers
    def handle_change(e : ft.Event[ft.DatePicker]):
        nonlocal due_date
        nonlocal today
    
        selected_date = e.control.value
        
        days = (selected_date - datetime.datetime.now(datetime.timezone.utc)).days
        print(f'Selected value got {selected_date}')
        
        print(f'Days calculated {days}')
        term.value = days
        term_title.value = f'Loan term days: {days} '
        page.update()
    def handle_dismissal(e: ft.Event[ft.DialogControl]):
        page.add(ft.Text('Date picker dismissed'))
    
    
    
    
    date_picker = ft.DatePicker(
        first_date=datetime.datetime(year =today.year -1 , month = 1, day = 1),
        last_date = datetime.datetime(year = today.year + 1, month = today.month ,day = 20),
        on_change =handle_change,
        on_dismiss = handle_dismissal
    )
# all field's titles
    loan_amount_title = ft.Text(
        'How much you going to lend:',
        size = 15,
        weight = ft.FontWeight.NORMAL,
        text_align = ft.TextAlign.START
    )
    print ('Title for loan amount field is created')

    term_title = ft.Text(
        'Loan term days:',
        size = 15,
        weight = ft.FontWeight.NORMAL,
        text_align = ft.TextAlign.START
    )
    print ('Title for term field is created')
    
    repay_title = ft.Text(
        'Your return',
        size = 15,
        weight = ft.FontWeight.NORMAL,
        text_align = ft.TextAlign.START
    )
    print ('Title for repay field is created')

# button
    back_button = ft.IconButton(
        icon = ft.Icons.ARROW_BACK,
        icon_size = 24,
        on_click = handle_back,

        tooltip = 'Back to Dashboard',
        icon_color = ft.Colors.GREY_800
    )


    send_agreement = ft.ElevatedButton(
        content = ft.Text('Send agreement'),
        color = ft.Colors.WHITE,
        on_click = handle_send_agreement,

        #button style
        style = ft.ButtonStyle(
            shape = ft.RoundedRectangleBorder(radius = 8),
            bgcolor = ft.Colors.AMBER
        )

    )


    print('Send agreement button is created')

# all containers
    
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

    # loan creation form
    loan_creation_form = ft.Container(
        content = ft.Column(
            [
                ft.Column(
                    [

                        loan_amount_title,
                        ft.Container(height = 8),
                        loan_amount
                    ],
                    horizontal_alignment  = ft.CrossAxisAlignment.CENTER,
                    spacing = 0
                ),
                ft.Container(height = 20),



                # term Section
                ft.Column(
                    [
                        term_title,
                        ft.Container(height = 8),
                        ft.Row( controls = [term , ft.Button(
                            content = 'Pick repay date',
                            icon = ft.Icons.CALENDAR_MONTH,
                            on_click = lambda e: page.show_dialog(date_picker),
                        )
                        ]
                        )
                    ],
                    horizontal_alignment  = ft.CrossAxisAlignment.START,
                    spacing = 0
                ),
                ft.Container(height = 20),
            
                # Repay section
                ft.Column(
                    [
                        repay_title,
                        ft.Container(height = 8),
                        repay
                    ],
                    horizontal_alignment  = ft.CrossAxisAlignment.CENTER,
                    spacing = 0
                ),
                
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            alignment = ft.MainAxisAlignment.CENTER,
            spacing = 0
            
        ),
        padding = 30,
        alignment = ft.Alignment.CENTER,
        bgcolor= ft.Colors.WHITE,
        border_radius = 16,
        shadow = ft.BoxShadow(
            spread_radius = 1,
            blur_radius = 10,
            color = ft.Colors.with_opacity(0.1 ,ft.Colors.BLACK),
            offset = ft.Offset(0, 4)
        )

        
    )

    return ft.View(
        route = '/loan_creation',
        bgcolor = ft.Colors.GREY_50,
        controls= [
            mobile_wrapper(
                ft.Column(
                    spacing = 16,
                    controls = [
                        header,
                        notification_title,
                        loan_creation_form,
                        send_agreement,
                        ft.Container(height = 20)
                    ],
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER
                )
            )
        ]
    )

'''
        containers plan

    Each field paired with it's title by ft.Row
    Then they stack in column and then placed in container

    Then all stacks in column 

        Air container 
        Main title / notification container
        Fields container
        Button
'''


'''
        PAGE PLAN

    Title = Create a loan

    Inputs: 
        Borrower : Borrower name ( Automatically apeared after serching )
        Loan amount : How much you lend ( User enter amount)
        Term: For how many days you will lend money (User enter days)
        Repay: How much you expected to earn from this loan how much borrower will overpay you ( user enter amount)

    Button:
        Send agreement ( will send to the borrower, after borrower accept , creates a loan)


'''

