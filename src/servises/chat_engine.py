import flet as ft
from dataclasses import dataclass
from servises.messanger_services import format_message_date, get_messages, send_message
from servises.user_servises import get_user_by_id
from Test import mobile_wrapper
@dataclass
class Message:
    sender_name: str
    sender_id: str
    content: str
    message_type: str
    sent_at: str
    reply_to: str = None

@ft.control
class ChatMessage(ft.Row):
    def __init__(self, message: Message, is_mine: bool):
        super().__init__()
        self.message = message
        self.is_mine = is_mine
        self.vertical_alignment = ft.CrossAxisAlignment.START

        if message.message_type == 'text':
            self.controls = self._build_text()
        elif message.message_type == 'contract_request':
            self.controls = self._build_contract_request()
        elif message.message_type =='contract_response':
            self.controls = self._build_contract_response()

    def _build_text(self):
        print("BUILD TEXT:", self.message.content)
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
    def _build_contract_request(self):
        return[
            ft.Card(
                content = ft.Container(
                    content = ft.Column( [
                        ft.Text('Loan request', weight = ft.FontWeight.BOLD),
                        ft.Text(self.message.content),
                        ft.Row([
                            ft.ElevatedButton('Agree'),
                            ft.OutlinedButton('Disagree')
                        ]) if not self.is_mine else ft.Text( 'waiting for response')
                    ]),
                    padding= 10
                )
            )
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

        self.message_list = ft.ListView(expand = True, spacing = 8 , auto_scroll = True, padding = ft.Padding.only(bottom = 120))
        self.input_field = ft.TextField (
            hint_text = 'Message..', expand = True,
            border_radius = 20,
            autofocus = True,
            min_lines = 1,
            max_lines = 5)
        self.back_button = None
    def _from_db(self, msg: dict):
        if 'users' in msg:
            sender_name = msg['users']['name']
        elif 'user_info' in msg:
            sender_name = msg['user_info']['name']
        else:
            sender_name = 'Uknown'
        return ChatMessage(
            message = Message(
                sender_id = msg['sender_id'],
                sender_name = sender_name,
                content = msg['content'],
                message_type = msg['type'],
                sent_at = msg['sent_at'],
                reply_to = msg.get('reply_to')
            ),
            is_mine = msg['sender_id'] == self.user.user_id
        )
    def append_message(self, msg: dict):
        # called realtime
        self.message_list.controls.append(self._from_db(msg))
        self.page.update()
    async def load_messages(self):
        messages = await get_messages(self.group_id)
        for msg in messages:
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
    
    def build(self):
        self.page.run_task(self.load_messages)

        input_bar = ft.Container(
            content = ft.Column([
               ft.IconButton(icon = ft.Icons.ATTACH_MONEY, on_click = None) if self.is_dm else ft.Container(),
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
