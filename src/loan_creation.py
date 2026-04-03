import flet as ft
import datetime
import asyncio


from Test import mobile_wrapper

from servises.sessions_services import(
    get_session,
    update_negotiation_details,
    set_agreement,
    complete_session,
    cancel_session,
    deactivate_session
)
from servises.user_servises import get_user_by_id
from servises.user import User
from servises.loan_services import insert_loan


def loan_creation_view(page : ft.Page): 

    # get user, session info and role

    user = page.data.get('User') if page.data else None
    session = page.data.get('session')
    session_id =page.data.get('session_id')
    role = page.data.get('role')

    # get date time from date picker
    today = datetime.datetime.now()
    due_date = None
    polling_active = True
# status text shows updates as negotiation process
    status_text = ft.Text(
        "Waitng borrower to join..." if role == 'lender' else "Review the details below",
        size = 14,
        color = ft.Colors.GREY_600,
        text_align = ft.TextAlign.CENTER
    )
    print('status label created')

    # show success or error mesages
    notification_title = ft.Text( # will show if loan created or not
        '',
        size = 40,
        weight = ft.FontWeight.NORMAL,
        text_align = ft.TextAlign.CENTER

    )
    print('notification title is created')

    # fields
    loan_amount_focused = False
    def on_loan_amount_focused(e):
        nonlocal loan_amount_focused
        loan_amount_focused = True
    def on_loan_amount_blur(e):
        nonlocal loan_amount_focused
        loan_amount_focused = False
    loan_amount = ft.TextField(
        label = '',
        width = 300,
        on_focus = on_loan_amount_focused,
        on_blur = on_loan_amount_blur
    )

    print('Loan amount form is created')
# creating borrower user from db data

    # forms handler

    def on_form_change(e):
        nonlocal due_date
        value = e.control.value
        if not value:
            return
        term_title.value = f"Loan term days: {value}"
        due_date = datetime.datetime.now() + datetime.timedelta(days = int(value))
        print(f'calculated due date: {due_date}')
        # calculate due_date by input days
        
        page.update()
    term_focused = False
    def on_term_focus(e):
        nonlocal term_focused
        term_focused = True
    def on_term_blur (e):
        nonlocal term_focused
        term_focused = False
    term = ft.TextField(
        label = '',
        width = 100,
        on_change = on_form_change,
        on_focus = on_term_focus,
        on_blur = on_term_blur
    )

    print('input loan term form is created')
    repay_focused = False
    def on_repay_focus(e):
        nonlocal repay_focused
        repay_focused = True
    def on_repay_blur(e):
        nonlocal repay_focused
        repay_focused = False
    repay = ft.TextField(
        label = '',
        width = 300
    )
    print('repay form is created')
    # pre-fill fields if the other side sent details
    if session:
        if session.get('amount'):
            loan_amount.value = str(session['amount'])
        if session.get('days'):
            term.value = str(session['days'])
            term_title.value = f"Loan term days: {session['days']}"
        if session.get('return'):
            repay.value = str(session['return'])

    # date picker 
    def handle_change(e : ft.Event[ft.DatePicker]):
        nonlocal due_date
        nonlocal today
    
        selected_date = e.control.value
        
        days = (selected_date - datetime.datetime.now(datetime.timezone.utc)).days
        print(f'Selected value got {selected_date}')
        
        print(f'Days calculated {days}')
        term.value = str(days)
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


# all titles and buttons and fields 
    main_title = ft.Text(
        'Create a Loan',
        size = 32,
        weight = ft.FontWeight.BOLD,
        text_align = ft.TextAlign.CENTER,
        color = ft.Colors.GREY_800
    )
    print('title is created')
    
    


# all field's titles
    
    loan_amount_title = ft.Text(
        'How much you going to lend:',
        size = 15,
        weight = ft.FontWeight.NORMAL,
        text_align = ft.TextAlign.START,
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
# send credit details button
    send_agreement = ft.Button(
        content = ft.Text('Send details'),
        disabled = role == 'lender', # True for lender, False for borrower
        color = ft.Colors.WHITE,

        #button style
        style = ft.ButtonStyle(
            shape = ft.RoundedRectangleBorder(radius = 8),
            bgcolor = ft.Colors.GREY_800
        )

    )
    print('Send agreement button is created')
# agreee button - if details is correct, hidden unltile details sent
    agree_button = ft.Button(
        content = ft.Text('Agree'),
        visible = False, # True after sent agreement
        style = ft.ButtonStyle(
            shape = ft.RoundedRectangleBorder(radius = 8),
            bgcolor = ft.Colors.GREEN
        )
    )
    print('agree button created, not visible yet')
# create loan button
    create_loan_button = ft.Button(
        content = ft.Text('Create loan'),
        visible = False,
        style = ft.ButtonStyle(
            shape = ft.RoundedRectangleBorder(radius = 8),
            bgcolor = ft.Colors.BLUE
        )
    )

# button
    back_button = ft.IconButton(
        icon = ft.Icons.ARROW_BACK,
        icon_size = 24,
        on_click = lambda e: page.run_task(go_back), 
        tooltip = 'Back to Dashboard',
        icon_color = ft.Colors.GREY_800
    )
# go back — stops polling, deactivates session, then navigates 
    async def go_back():
        nonlocal polling_active
        polling_active = False
        if session_id and role:
            await deactivate_session(session_id, role)
            print('session is deactivated')
            s = await get_session(session_id)
            if s and s.get('status') != 'complete':
                await cancel_session(session_id)
                print('session cancelled')
        await page.push_route('/dashboard')
        print('Navigated to dashboard')
    back_button.on_click = lambda e: page.run_task(go_back)
# borrower left popup to lender notification when session is cancelled (borrower dismissed invitation)
    async def show_borrower_left_popup():
        def handle_ok(e):
            dialog.open = False
            page.update()
            page.run_task(go_back)
        # popup message dialog
        dialog = ft.AlertDialog(
            title = ft.Text('Borrower left'),
            content = ft.Text('The borrower dismissed invitation. Taking you back to dashboard'),
            actions = [ft.TextButton('Ok', on_click = handle_ok)]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
    # on load function to get boorower data from db and create and object 
        
    # polling — both sides watch the same session, but for different things ─
    async def start_polling():
        nonlocal polling_active
        while polling_active:
            try:
                # getting current session info
                sid = page.data.get('session_id')
                print(f'polling with session_id: {sid}')
                if not sid:
                    await asyncio.sleep(1)
                    continue
                s = await get_session(session_id)

                if not s or s.get('status') =='canceled':
                    if role == 'lender':
                        await show_borrower_left_popup()
                    return

                # lender fuctions
                if role == 'lender':
                    # watch for borrower sending updated number
                    if s.get('amount') and s.get('last_updated_by') == 'borrower':
                        agree_button.visible = True
                        if not loan_amount_focused and loan_amount.value != str(s['amount']):
                            loan_amount.value = str(s['amount'])
                        if not term_focused and term.value != str(s['days']):
                            term.value = str(s['days'])
                            term_title.value = f"Loan term days: {s['days']}"
                        if not repay_focused and repay.value !=str(s['return']):
                            repay.value = str(s['return'])
                        status_text.value = 'Borrower sent updated details'
                        page.update()
                    # unlock send agreement button if borrwer joined, changing status
                    if s.get('borrower_active') and send_agreement.disabled:
                        send_agreement.disabled = False
                        
                        status_text.value = 'Borrower is here, you can now send agreement details'
                        page.update()
                    
                    # show agree when borrower agreed 
                    if s.get('borrower_agree') and not agree_button.visible:
                        agree_button.visible = True
                        status_text.value = 'Borrower agreed, Press Agree to confurm the deal'
                        page.update()

                # borrower functions
                if role == 'borrower':
                    # show if lender send another change
                    if s.get('amount') and s.get('last_updated_by') == 'lender':
                        agree_button.visible = True
                        if not loan_amount_focused and loan_amount.value != str(s['amount']):
                            loan_amount.value = str(s['amount'])
                        if not term_focused and term.value != str(s['days']):
                            term.value = str(s['days'])
                            term_title.value = f"Loan term days: {s['days']}"
                        if not repay_focused and repay.value !=str(s['return']):
                            repay.value = str(s['return'])
                        status_text.value = 'Lender sent updated details'
                        page.update()


                    
                     # show Agree when lender has agreed
                    if s.get('lender_agree') and not agree_button.visible:
                        agree_button.visible = True
                        status_text.value = 'Lender agreed, Press Agree to confurm the deal'
                        page.update()
                    # lock borrower view
                    if s.get('lender_agree') and s.get('borrower_agree'):
                        send_agreement.visible = False
                        agree_button.visible = False
                        loan_amount.read_only = True
                        term.read_only = True
                        repay.read_only = True
                        status_text.value = 'Both agreed, waiting for lender to confirm'
                        page.update()
            except Exception as e:
                print(f"polling error: {e}")

            await asyncio.sleep(2)
    
    # send details

# event after send agreement click
    async def handle_send_agreement(e):

    # debugging
        print('send agreement is clicked')
        print(f'Current route {page.route}')
        
        if not loan_amount.value or not term.value or not repay.value:
            notification_title.value = 'Please fill all fields'
            notification_title.color = ft.Colors.RED_400
            page.update()
            return
        await update_negotiation_details(
            session_id =session_id,
            loan_amount = int(loan_amount.value),
            days = int(term.value),
            loan_due_date = due_date.isoformat() if due_date else None,
            return_amount = int(repay.value),
            updated_by = role
        )
        agree_button.visible = False
        status_text.value = 'Details sent- waiting other side to agree'
        page.update()
    send_agreement.on_click = handle_send_agreement

        
    async def handle_create_loan(e):
        await complete_session(session_id)

    # create a loan and take change balance
        borrower_data = page.data.get('borrower')
        borrower_user = User(
            user_id = borrower_data['id'],
            user_name = borrower_data['name'],
            user_phone = borrower_data['phone_number'],
            balance = borrower_data['balance'])

        result = await user.lend_money_short(
            amount = int(loan_amount.value),
            term = int(term.value),
            repay = int(repay.value),
            debtor = borrower_user,
            loan_due_date = due_date.isoformat() if due_date else None,
            loan_session_id = session_id
            )
        print('Balance changed and money lended')
    # showing that loan is created
        notification_title.value = result
        # change color dependong on success
        if 'succesfully' in result.lower():

            notification_title.color = ft.Colors.GREEN_400
        else:
            notification_title.color = ft.Colors.RED_400
        create_loan_button.visible = False
        status_text.value = 'Loan created'
        page.update()
        await asyncio.sleep(2)
        await go_back()
    create_loan_button.on_click = handle_create_loan

    # agree actions
    async def handle_agree(e):
        s = await set_agreement(session_id, role)
        
        if s.get('lender_agree') and s.get('borrower_agree'):
            # both agree we hide Send and agre , show Loan creation button
            send_agreement.visible = False
            agree_button.visible = False

            # view depend on role ( if lender show Create loan if borrwer just wait)
            if role == 'lender':
                create_loan_button.visible = True
                status_text.value = 'Both agreed, Press Create loan to finalize'
                
            else:
                # borrower side- just show confirmation
                status_text.value = "Both agreed!, Waiting for lender confirmation"
                loan_amount.read_only = True
                term.read_only = True
                repay.read_only = True
            page.update()

        else:
            # only one side agreed so far
            send_agreement.visible = False
            agree_button.visible = False
            status_text.value = 'You agreed, waiting for other side'
            page.update()
    agree_button.on_click = handle_agree

    # start polling when page loads
    page.run_task(start_polling)
    




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
                            content = ft.Text('Pick repay date'),
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
                        status_text,
                        notification_title,
                        loan_creation_form,
                        send_agreement,
                        agree_button,
                        create_loan_button,
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

