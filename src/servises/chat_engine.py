'''
Triggesr FOR DIFFERENT MESSAGE TYPES
        LENDING CONTRACT APPLICATION = 'loan_contract'
        UPDATING L-CONTRACTS = 'contract_response'



        Lending trough  message logic:

    1) creating a loan application session via POST (lender_id = userA_id, borrower_id = userB_id, amount , days, return = Optional)

    
   To create a loan i need
   Borrower class -> borrower data (
   borrower_user = User(
            user_id = borrower_data['id'],
            user_name = borrower_data['name'],
            user_phone = borrower_data['phone_number'],
            balance = borrower_data['balance'])) 
             -> so i need to store local data for every dm  
               OR i can fetch data every time i have partner id
               i call get_user_by_id
                   
            THEN I CAN CREATE A USER CLASS with borrower

            after that
            Update message ( by id)
            status : complete
            buttons - OFF

            all that via non local agree botton etc


    To update application results,

    send new message or  update current?

    if send new, we have to 
    
                         
                   '''

import flet as ft
from dataclasses import dataclass
from servises.messanger_services import format_message_date, get_messages, send_message, get_dm_partner
from servises.sessions_services import create_session, get_session, complete_session , cancel_session
from servises.user_servises import get_user_by_id
from Test import mobile_wrapper
from servises.user import User
from typing import Optional, Callable
from datetime import datetime


from finance_dialog import FinanceDialog
import datetime
from real_time import realtime_manager


@dataclass
class Message:
    id: str
    group_id: str
    sender_name: str
    sender_id: str
    content: str
    message_type: str
    sent_at: str
    user : object
    reply_to: str = None
    financial_product_code: str = None
    fin_product: dict = None
    disagree_handler: Optional[Callable] = None

    


@ft.control
class ChatMessage(ft.Row):
    def __init__(self, message: Message, is_mine: bool):
        super().__init__()
        self.message = message
        self.is_mine = is_mine
        self.vertical_alignment = ft.CrossAxisAlignment.START

        if message.message_type == 'text':
            self.controls = self._build_text()
        elif message.message_type == 'loan_contract' and message.fin_product:
            
            self.controls = self._build_loan_contract()
        elif message.message_type =='contract_response':
            self.controls = self._build_contract_response()

    def _build_text(self):
        sender_name = ft.Container()
        bubble = ft.Container(
            content = ft.Column(
                tight = True,
                spacing = 5,
                controls = [
                    sender_name if self.is_mine else ft.Text(self.message.sender_name, weight = ft.FontWeight.BOLD),
                    ft.Text(self.message.content,selectable= True),
                    ft.Text(format_message_date(self.message.sent_at), size = 10 , color = ft.Colors.GREY)
                    ]
                ),
                bgcolor = ft.Colors.BLUE_100 if self.is_mine else ft.Colors.GREY_200,
                border_radius = 12,
                padding =10
                )
        avatar = ft.CircleAvatar (

            content = ft.Text(self.get_initials(self.message.sender_name)),
            color = ft.Colors.WHITE,
            bgcolor = self.get_avatar_color(self.message.sender_name),
                )
        if self.is_mine:
            return [
                ft.Container(expand = True),
                bubble
            ]
        else:
            return [
                avatar,
                bubble
            ]
    def _show_option_menu(self, e):

        bottom_sheet = ft.BottomSheet(
            content = ft.Container(
                content = ft.Column(
                    [
                        ft.ListTile(
                            leading = ft.Icons.EDIT_OUTLINED,
                            title= ft.Text('Edit contract'),
                            on_click = None # here we add edit functions
                        ),
                        ft.Divider(height = 1),
                        ft.ListTile(
                            leading = ft.Icon(ft.Icons.DELETE_OUTLINE, color = ft.Colors.RED),
                            title = ft.Text('Delete', color = ft.Colors.RED),
                            on_click = None # here i add delete function
                        )

                    ],
                    tight = True,
                    spacing = 8
                ),
                padding = ft.Padding.only(bottom = 16),
                width = 380
            ),
            
            open = True,
            on_dismiss = lambda e: None
        )
        self.page.overlay.append(bottom_sheet)
        self.page.update()
    def disable_buttons(self, update: bool = False):
        if hasattr(self, 'actions_row'):
            self.actions_row.controls = [
                ft.Text('Cancelled', color = ft.Colors.RED, size = 12)
                if self.message.fin_product and self.message.fin_product['status'] == 'canceled' or self.message.fin_product['status'] == 'pending'
                else ft.Text('Loan created successfully', color  = ft.Colors.GREEN, size = 12)
            ]
            if update:

                self.actions_row.update()
    # if i send a contract request
    def _build_loan_contract(self):
        
        avatar = ft.CircleAvatar (

            content = ft.Text(self.get_initials(self.message.sender_name)),
            color = ft.Colors.WHITE,
            bgcolor = self.get_avatar_color(self.message.sender_name),
                )
        
        
        agree_button = ft.Button(ft.Text('Agree', color = ft.Colors.WHITE),bgcolor = ft.Colors.GREEN, on_click = self._handle_create_loan)
        disagree_button = ft.Button(ft.Text('Disagree', color = ft.Colors.WHITE), bgcolor = ft.Colors.RED, on_click = self._handle_disagree_loan)
        edit_button = ft.Button(ft.Text('Edit', color = ft.Colors.WHITE), bgcolor = ft.Colors.BLUE)
        cancel_button = ft.Button(ft.Text('Cancel', color = ft.Colors.WHITE), bgcolor = ft.Colors.RED, on_click= self._handle_disagree_loan)

        if self.message.fin_product['status'] == 'complete':
            self.actions_row = ft.Row(
                controls = [
                    ft.Text('Loan Created successfully', color = ft.Colors.GREEN)
                ]
            )

            contract_status = ft.Text(f'{self.message.fin_product['status']}', color = ft.Colors.GREEN, size = 10)


        else:
            self.actions_row = ft.Row(
                controls = [
                    edit_button,
                    cancel_button
                ] if self.is_mine else [
                    agree_button,
                    disagree_button
                ],
                alignment = ft.MainAxisAlignment.CENTER
            )
            
            
            contract_status = ft.Text(f'{self.message.fin_product['status']}', color = ft.Colors.GREY, size = 10)
        
        contract = ft.Card( content = 
                           ft.Container(
                content = ft.Column([
                    ft.Text(self.message.sender_name,  weight = ft.FontWeight.BOLD) if not self.is_mine else ft.Container(),
                    ft.Text('Loan contract',weight = ft.FontWeight.BOLD, size = 15 ),
                    ft.Row( # contract amount and days
                        controls = [
                            ft.Container( # contract amount
                                content = ft.Column(
                                    [
                                        ft.Text(f'{self.message.fin_product['amount']}',color = ft.Colors.GREEN, size = 25,  weight = ft.FontWeight.BOLD),
                                        ft.Text('som', size = 16)
                                    ],
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                    spacing = 0
                                ),
                                bgcolor = ft.Colors.WHITE,
                                padding = 20,
                                border_radius = 25,
                                expand= True
                            ),
                            ft.Container( # contract days
                                content = ft.Column(
                                    [
                                        ft.Text(f'{self.message.fin_product['days']}',size = 25, weight = ft.FontWeight.BOLD),
                                        ft.Text('days', size = 16)
                                        
                                    ],
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                    spacing = 0
                                ),
                                bgcolor = ft.Colors.WHITE,
                                padding = 20,
                                border_radius = 25,
                                expand= True
                            )
                        ]
                    ),
                    ft.Row(
                        controls = [
                            ft.Container(
                                content = ft.Column(
                                    controls = [
                                        ft.Text(f'{self.message.fin_product['return'] if self.message.fin_product['return'] > 0 else '---'}', color = ft.Colors.BLUE, size = 25, weight = ft.FontWeight.BOLD),
                                        ft.Text('return', size =16)
                                    ],
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                    spacing = 0
                                ),
                                bgcolor = ft.Colors.WHITE,
                                padding = 20,
                                border_radius = 25,
                                expand= True
                            )
                        ],
                        alignment = ft.MainAxisAlignment.CENTER
                    ),
                    self.actions_row, # if it is mine true we show only EDIT OR CANCEL BUTTONS, on the other hand we show agree or disagree
                    ft.Row(
                        controls = [
                            contract_status,
                            ft.Text(format_message_date(self.message.sent_at), size = 10 , color = ft.Colors.GREY)
                        ],
                        alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ],
                tight = True,
                spacing = 6,
                expand = True
                ),
                padding = 12,
                width = 260
            )

        )

        interactive_card = ft.GestureDetector(
            content = contract,
            on_long_press = self._show_option_menu,
            on_secondary_tap = self._show_option_menu
        )

        
        if self.is_mine:
            return [
                ft.Container(expand= True),
                interactive_card
            ]
        else:
            return [
                avatar,
                interactive_card
            ]
        

    # if user reply to that contract
    def _build_contract_response(self):
        return [
            ft.Card(
                content = ft.Container(
                    content =  ft.Text(self.message.content),
                    padding = 10
                )
            )
        ]
    # async handle loans page : after succesfuly creating a loan show shortcut button to navigate user 

    async def _handle_disagree_loan(self, e):
        await self.message.disagree_handler(
            fin_product_code= self.message.financial_product_code,
            is_mine = self.is_mine, 
            group_id = self.message.group_id,
            reference_contract_message_id = self.message.id

        )
    
    # here we adding agree for loan handler
    async def _handle_create_loan(self,e):

# first we fetch borrower data
        lender_data =  await get_user_by_id(self.message.sender_id)
        print(f'Succesfuly fetch lender data: {lender_data}')
        lender_user = User(
            user_id = lender_data['id'],
            user_name = lender_data['name'],
            user_phone = lender_data['phone_number'],
            balance = lender_data['balance'],
        )
        
        print(f'Succesfuly created lender class: {lender_user.info()}')
        print(f'This is session is about complete: {self.message.financial_product_code}')
        
        updated_session = await complete_session(self.message.financial_product_code) 

        
        print(f'This is updated sessopn: {updated_session}') 

        # here we are creating a loan
        loan_result = await lender_user.lend_money_short(
            amount = updated_session['amount'],
            term = updated_session['days'],
            repay = updated_session['return'],
            loan_due_date = updated_session['due_date'],
            loan_session_id = updated_session['id'],
            debtor = self.message.user
            )
        
        # sending message
        await send_message(
            group_id = self.message.group_id,
            sender_id = self.message.user.user_id,
            content = f'{self.message.user.user_name} agreed to the loan',
            reply_to = self.message.id,
            financial_product_code = updated_session['id']
        )
        
        # here we update that message
        
        
        #await get_session(self.message.financial_product_code)  
        #print(f'This session is complete: )
    
    

    def get_initials(self, user_name:str):
        if user_name:
            return user_name[:1].capitalize()
        else:
            return 'Unknown'
    def get_avatar_color(self, user_name:str):
        colors_lookup = [
            ft.Colors.AMBER,
            ft.Colors.BLUE,
            ft.Colors.BROWN,
            ft.Colors.CYAN,
            ft.Colors.GREEN,
            ft.Colors.INDIGO,
            ft.Colors.LIME,
            ft.Colors.ORANGE,
            ft.Colors.PINK,
            ft.Colors.PURPLE,
            ft.Colors.RED,
            ft.Colors.TEAL,
            ft.Colors.YELLOW
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]
    
class Chat:
    def __init__(self, page, user ):
        self.page = page
        self.user = user
        self.user_name  = None
        self.group = page.data['current_group']
        self.group_id = self.group['group_id']
        self.is_dm = self.group['groups']['type'] == 'dm'
        self.display_name = self.group.get('display_name') if self.is_dm else self.group['groups']['name']
        self.display_id = self.group.get('display_id') if self.is_dm else 'No id to display'

        self.messages = []
        self.message_controls = {}
        self.message_list = ft.ListView(expand = True, spacing = 8 , auto_scroll = True, padding = ft.Padding.only(bottom = 120))

        self.input_field = ft.TextField (
            hint_text = 'Message..', expand = True,
            border_radius = 20,
            autofocus = True,
            min_lines = 1,
            max_lines = 5)
        self.back_button = None

    async def handle_disagree_button(self, fin_product_code, is_mine , group_id , reference_contract_message_id):
            updated_session  = await cancel_session(fin_product_code)

            # send message that this loan contract was canceld by borrower

            await send_message(
                group_id = group_id,
                sender_id = self.user.user_id,
                content = f'{self.user.user_name} canceled the contract',
                reply_to = reference_contract_message_id,
                financial_product_code = fin_product_code
            )

    def _from_db(self, msg: dict, fin_product: dict = None):
        if 'users' in msg:
            
            sender_name = msg['users']['name']
        elif 'user_info' in msg:
            sender_name = msg['user_info']['name']
        else:
            sender_name = 'Uknown'
        
        # here i need to chek for different type of message : if lend money message one type, if money request, another.
        print(f'THis is checking msg: {msg}')
        print(f'Got fin product: {fin_product}')
        return ChatMessage(
            message = Message(
                id = msg.get('id'),
                group_id = self.group_id,
                sender_id = msg['sender_id'],
                sender_name = sender_name,
                content = msg['content'],
                message_type = msg['type'],
                sent_at = msg['sent_at'],
                reply_to = msg.get('reply_to'),
                financial_product_code =  msg['financial_product_code'],
                fin_product = fin_product,
                user = self.user,
                disagree_handler = self.handle_disagree_button
            ),
            is_mine = msg['sender_id'] == self.user.user_id
        )
    def update_contract_message(self, application_session: dict):
        print(f'Got updated session: {application_session}')
    
    def on_new_application_session(self, application_session: dict):
        print(f'Got new session: {application_session}')


    def append_message(self, msg: dict):
        product = msg.get('fin_product')
        fin_code = msg.get('financial_product_code')
        # called realtime
        if fin_code:
            for old_msg in self.messages:
                if old_msg.get('financial_product_code') == fin_code:
                    control = self.message_controls.get(old_msg['id'])
                    if control:
                        self.mark_as_updated(control)
        

        new_control = self._from_db(msg, fin_product = product)
        self.messages.append(msg)
        self.message_controls[msg['id']] = new_control
        self.message_list.controls.append(new_control)

        self.page.update()
    def mark_as_updated(self, control):
        control.opacity = 0.4
        if hasattr(control, 'disable_buttons'):
            control.disable_buttons(update = True)       
        control.update()
    def parse_date(self, sent_at: str):
        sent_at = sent_at.replace(' ', 'T')
        sent_at = sent_at.split('+')[0]
        return datetime.datetime.fromisoformat(sent_at)
    async def load_messages(self):
        messages = await get_messages(self.group_id)

        session_cache: dict [str, dict] = {}
        latest_per_fin_code : dict [str, str] = {}

        for msg in messages:

            fin_code = msg.get('financial_product_code')
            if fin_code:
                existing = latest_per_fin_code.get(fin_code)
                if not existing:
                    latest_per_fin_code[fin_code] = msg['id']
                else:
                    existing_msg = next(m for m in messages if m['id'] == existing)
                    if self.parse_date(msg['sent_at']) > self.parse_date(existing_msg['sent_at']):
                        latest_per_fin_code[fin_code] = msg['id']

        for msg in messages:
            fin_code = msg.get('financial_product_code')

            if msg['type'] == 'loan_contract' and  fin_code:
                if fin_code not in session_cache:
                    session_cache[fin_code] = await get_session(fin_code)
                
                product =  session_cache[fin_code]
                control = self._from_db(msg, product)

                if product and product['status'] in ('canceled', 'complete'):
                    if hasattr(control, 'disable_buttons'):
                        control.disable_buttons(update = False)
               
            else:
                #print(f'This is type of session: {type(product)}')
                control = self._from_db(msg)
            
            if fin_code and latest_per_fin_code.get(fin_code) != msg['id']:
                control.opacity = 0.4

            self.messages.append(msg)
            self.message_controls[msg['id']] = control
            self.message_list.controls.append(control)
        self.page.update()

    async def send_message(self, e):
        if not self.input_field.value:
            return
        await send_message(group_id = self.group_id,
                           sender_id = self.user.user_id,
                           content = self.input_field.value,
                           message_type = 'text'
                           )
        
        self.input_field.value = ''
        self.page.update()
    def finance_layer(self, e):
        finance_layer = FinanceDialog(
        page = self.page,
        user = self.user,
        group_id = self.group_id,
        parthner_id = self.display_id
        )
        finance_layer.open(e)
        
    
    def build(self):
        self.page.run_task(self.load_messages)

        input_bar = ft.Container(
            content = ft.Column([
                ft.Row([ft.IconButton(icon = ft.Icons.ATTACH_MONEY, on_click = self.finance_layer) if self.is_dm else ft.Container()]),
                ft.Row([
                    self.input_field,
                    ft.IconButton(ft.Icons.SEND, on_click = self.send_message)
            ])
        ]) )
        

        return ft.View(
            route ='/chat',
            controls = [
                mobile_wrapper(
                    ft.Column(
                        expand = True,
                        spacing = 0,
                        height = self.page.height,
                        controls = [
                            ft.AppBar(actions = self.back_button,
                                      title = ft.Text(self.display_name)),
                            ft.Column(
                                expand = True,
                                controls = [
                                    self.message_list,
                                    input_bar
                            ]
                    

                          )
                        ]
                     )
                )
             ]
        )
