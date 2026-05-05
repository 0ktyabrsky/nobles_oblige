import flet as ft
from servises.sessions_services import create_session
from servises.messanger_services import send_message


class FinanceDialog:
    def __init__ (self, page: ft.Page, user, group_id, parthner_id):
        self.page = page
        self.user = user
        self.group_id = group_id
        self.parthner_id = parthner_id
        self.current_tab = 0

        self.user_balance = self.user.balance



        # transaction


        # lend money
        self.loan_contract_amount = ft.TextField(label = 'How much to lend...', keyboard_type = ft.KeyboardType.NUMBER)
        

        self.loan_contract_days = ft.TextField(label = 'for how many days', keyboard_type = ft.KeyboardType.NUMBER)
        
        self.loan_contract_return = ft.TextField(label  = 'How much to charge', keyboard_type = ft.KeyboardType.NUMBER)
        

        # FinanceDialog

        self.tabs_control = self._build_tabs()
        self.dialog = self._build_dialog()
        

    
    
    def _build_tabs(self):
        def on_tab_change (e):
            self.current_tab  =e.control.selected_index
            
        return ft.Tabs(
            #selected_index = 2,
            length = 3,
            expand = True,
            on_change = on_tab_change ,
            content = ft.Column(
                expand = True,
                controls = [
                    ft.TabBar(
                    
                        tabs = [
                            ft.Tab(label = 'transfer' ),
                            ft.Tab(label = 'lend'),
                            ft.Tab(label = 'request')
                        ]
                    ),
                    ft.TabBarView(
                        height= 180 ,
                        controls = [
                            # transfer money
                            ft.Column(
                                controls= [
                                    ft.Text('This is transfer tab')
                                ]

                            ),
                            # lend money tab
                            ft.Column(
                                controls = [
                                    
                                    self.loan_contract_amount,
                                    
                                    self.loan_contract_days,
                                    
                                    self.loan_contract_return
                                ],
                                spacing = 12,
                                horizontal_alignment = ft.CrossAxisAlignment.CENTER
                            ),
                            ft.Column(
                                controls = [
                                    ft.Text('this is money request tab')
                                ]
                            )
                        ]
                    )
                ]
            )
        )
    def _build_dialog(self):
        return ft.AlertDialog(
            modal = False,
            title = ft.Text(f'balance: {self.user_balance}',text_align = ft.TextAlign.CENTER, size = 24),
            content = ft.Container(
                content= self.tabs_control,
                height = 250
                ),
                actions = [
                    ft.Button(
                        content = 'Send',
                        on_click = self._on_send
                    )
                ],
                actions_alignment = ft.MainAxisAlignment.END
            

        )
    
    async def _on_send(self):
        tab = self.current_tab
        
        if tab == 0:
            print(f'this is a button from tabs {tab}')
        elif tab == 1:
            print(f'this is a button from tabs {tab}')
            
            new_loan_application = await create_session(
                self.user.user_id,
                self.parthner_id,
                self.loan_contract_amount.value,
                self.loan_contract_days.value,
                self.loan_contract_return.value
            )
            print(f'this is newly created loan application: {new_loan_application['id']}')
            await send_message(
                self.group_id,
                self.user.user_id,
                content = f'{self.user.user_name} lending money',
                message_type = 'loan_contract',
                financial_product_code = new_loan_application['id'] if new_loan_application else None
            )
        
            

        elif tab == 2:
            print(f'this is a button from tabs {tab}')
        self.dialog.open = False
        self.page.update()

    def open (self, e):
        self.page.show_dialog (self.dialog)
        self.page.update()
    
    



'''
Plan for finance dialog class

        4 INPUTS
        PAGE
        USER OBJECT
        GROUP ID
        PARTHNER ID


        3 SECTIONS
        TRANSFER MONEY
        LEND MONEE
        MONEY REQUEST

        1 BUTTON
        SEND

    1. TRANSFER MONEY
    input amoun of money
    input comment on transaction

    2. LEND MONEY
    input amount to lend
    input the contract period in days
    input return amount

    3. MONEY REQUEST
    input amount to request
    input the conract period in days
    input return amount

        SEND BUTTON
    1. FOR TRANSFER MONEY
    create transaction in db
    send message(group_id , sender_id , content = comment on transaction , message_type = 'money transfer', reply_to = Optional, financial_product_id= transfer_id)

    2. FOR LEND MONEY
    create_session(lender_id, borrower_id, amount, days, amount_return)
    send message(group_id , sender_id , content = None , message_type = 'loan_contract', reply_to = Optional, financial_product_id= session_id)

    3 FOR MONET REQUEST

    

        CLASS STRUCTURE

    every self parameter is a function that dinamicly create a finance layer
    self.dialog = def build dialog (): retrun alertdiaog
    inside that dialog there is a tabs and thery are in control of dialog
    self.tabs_control = def build tabs (): return tabs 
    every tab contain special fields that depends on tab type ( transaction, lend, request)
     





'''

