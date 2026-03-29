import flet as ft
# the login function
# the size of the phone 
from Test import mobile_wrapper
from servises.user import User
from servises.user_servises import get_user_by_phone , create_user
from stored.store import save_user
import asyncio



def login_view(page: ft.Page):
    
        # handeling sign in 
    async def handle_sign_in(e):
        
# Debuggin
        print('Sign in clicked')
        print(f'Current route {page.route}')
    
        # gettin data from all text fileds to create User
        name = user_name.value # get text from the fields
        phone = user_phonenumber.value
        print('User name and phone nuber got successfuly')


        #validation
        if not name or not phone:
            print('Please fill in all fields')
            return 
        # creating user 
       
        user = User.from_phone(name, phone)
        # debugging
        
        print(f'User name: {user.user_name}')
        print(f"User's phone number: {user.user_phone}")

        # storing users data
        save_user(user.user_id, phone, user.user_name)
        page.data = {
            "User" : user}
        print(user)
    
        #navigate to the dashboard
        await page.push_route('/dashboard')
        print('Navigated to dashboard')

    
    # title for a login and sign in, here only sign in
    title= ft.Text(
        'Registration' ,
         size = 40,
         weight = ft.FontWeight.NORMAL,
         text_align = ft.TextAlign.CENTER
        )
    
    print('Title created')
    # User name for profile
    user_name = ft.TextField(
        label = "Enter your name",
        width = 300
    
        # store the user name in BD to show it in the main SCREEN
    )
    print('User name form created')

    # User's phone number to lend money
    user_phonenumber = ft.TextField(
        label = 'Phone number +996',
        width = 300
        # only nuber data
    )
    print('User phone number form created')

    # sign in button
    sign_in = ft.Button(
        content = ft.Text("Sign in"),
        color = ft.Colors.WHITE,
        on_click = handle_sign_in,
        # check data for any issue
        # transfer user to the dachboard

        #button style
        style = ft.ButtonStyle(
            shape = ft.RoundedRectangleBorder(radius = 8),
            bgcolor = ft.Colors.AMBER
        )
    
    )
    print( 'sign in button created')

    
    #main container that will have 4 things: Main titile, Input name, Input phone number, sign in
    main_container = ft.Container(
        # all content will be in one columnn 
        content =ft.Column( [
            title,
            user_name,
            user_phonenumber,
            sign_in
        ],
        # define how does entities inside column will look
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        spacing = 10
        ),
        # discribe how this sign in container will look
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
        route ='/login',
        controls = [
            mobile_wrapper(
                ft.Column(
                    spacing = 16,
                    controls =[
                        main_container
                            ] 
                )
            )
        ]
    )
