'''
Triggesr FOR DIFFERENT MESSAGE TYPES
        LENDING CONTRACT APPLICATION = 'loan_contract'
        UPDATING L-CONTRACTS = 'contract_response'



        Lending trough  message logic:

    1) creating a loan application session via POST (lender_id = userA_id, borrower_id = userB_id, amount , days, return = Optional)
'''

import flet as ft
from dataclasses import dataclass
from servises.messanger_services import format_message_date, get_messages, send_message, get_dm_partner
from servises.sessions_services import create_session, get_session
from servises.user_servises import get_user_by_id
from Test import mobile_wrapper

from finance_dialog import FinanceDialog

@dataclass
class Message:
    sender_name: str
    sender_id: str
    content: str
    message_type: str
    sent_at: str
    reply_to: str = None
    financial_product_code: str = None
    fin_product: dict = None


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
    # if i send a contract request
    def _build_loan_contract(self):
        avatar = ft.CircleAvatar (

            content = ft.Text(self.get_initials(self.message.sender_name)),
            color = ft.Colors.WHITE,
            bgcolor = self.get_avatar_color(self.message.sender_name),
                )
        
        
        agree_button = ft.Button(ft.Text('Agree', color = ft.Colors.WHITE),bgcolor = ft.Colors.GREEN)
        disagree_button = ft.Button(ft.Text('Disagree', color = ft.Colors.WHITE), bgcolor = ft.Colors.RED)
        edit_button = ft.Button(ft.Text('Edit', color = ft.Colors.WHITE), bgcolor = ft.Colors.BLUE)
        cancel_button = ft.Button(ft.Text('Cancel', color = ft.Colors.WHITE), bgcolor = ft.Colors.RED)
        sender_actions = ft.Row(
                        controls = [
                            edit_button,
                            cancel_button
                        ],
                        alignment = ft.MainAxisAlignment.CENTER
                    )
        parthner_actions = ft.Row(
                        controls = [
                            agree_button,
                            disagree_button
                        ],
                        alignment = ft.MainAxisAlignment.CENTER
                    )
        contract = ft.Card( content = ft.Container(
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
                    sender_actions if self.is_mine else parthner_actions,
                    ft.Row(
                        controls = [
                            ft.Text(f'status: {self.message.fin_product['status']}', color = ft.Colors.GREY, size = 10),
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
        if self.is_mine:
            return [
                ft.Container(expand= True),
                contract
            ]
        else:
            return [
                avatar,
                contract
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

        self.message_list = ft.ListView(expand = True, spacing = 8 , auto_scroll = True, padding = ft.Padding.only(bottom = 120))
        self.input_field = ft.TextField (
            hint_text = 'Message..', expand = True,
            border_radius = 20,
            autofocus = True,
            min_lines = 1,
            max_lines = 5)
        self.back_button = None
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
                sender_id = msg['sender_id'],
                sender_name = sender_name,
                content = msg['content'],
                message_type = msg['type'],
                sent_at = msg['sent_at'],
                reply_to = msg.get('reply_to'),
                financial_product_code =  msg['financial_product_code'],
                fin_product = fin_product
            ),
            is_mine = msg['sender_id'] == self.user.user_id
        )

    def append_message(self, msg: dict):
        product = msg.get('fin_product')
        # called realtime
        self.message_list.controls.append(self._from_db(msg, fin_product = product))
        self.page.update()
    async def load_messages(self):
        messages = await get_messages(self.group_id)
        for msg in messages:
            print(f'this is messages from Db:{msg}')
            if msg['type'] == 'loan_contract' and msg['financial_product_code']:
                product =  msg.get('fin_product')
                self.message_list.controls.append(self._from_db(msg, product))
            else:
                #print(f'This is type of session: {type(product)}')
                self.message_list.controls.append(self._from_db(msg))
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
