import flet as ft
from login import login_view
from dashboard import dashboard_view
from lend_money import lend_money_view
from loan_creation import loan_creation_view
from investments import investments_view
from borrow_money import borrow_money_view
from loan_request import loan_request_view
from loans import loans_view
from stored.store import load_user
from  servises.user import User
from dashboard_2 import dashboard_2_view

# from investments import investments_view
# from loans import loans_view


# navigating all pages 

async def main(page: ft.Page):    
    # window width and heights for android apps
    page.window_width = 390
    page.window_height = 844
    print("App started!")
    #getting saved user's id
    saved_user = load_user()
    print(f"this is saved data{saved_user}")

   
    page.title = 'My App'
    page.bgcolor = ft.Colors.BLACK



    #route changing 
    def route_change(route):
        #debugging
        print(f'Route changed to {page.route}')
        # remove all pages 
        page.views.clear()

        # check if initital page is dashboard
        if page.route == '/dashboard':
            print('showing dashboad')
            page.views.append(dashboard_view(page))
        # showing lend money
        elif page.route == '/lend_money':
            print('showing lend money page')
            page.views.append(lend_money_view(page))
        # showing loan creation page
        elif page.route == '/loan_creation':
            print('Showing loan creation route')
            page.views.append(loan_creation_view(page))
        elif page.route == '/investments':
            print('Showing invetsments page')
            page.views.append(investments_view(page))
        elif page.route == '/borrow_money':
            print('Showing request money pgae')
            page.views.append(borrow_money_view(page))
        elif page.route == '/loan_request':
            print('showing loan request page')
            page.views.append(loan_request_view(page)),
        elif page.route =='/loans':
            print('showing  loans page')
            page.views.append(loans_view(page))
        elif page.route =='/dashboard_2':
            print('shoving dashboard_2 page')
            page.views.append(dashboard_2_view(page))

        else:
            print('showing login') 
            page.views.append(login_view(page))
        

        page.update()

    page.on_route_change = route_change
    await page.push_route('/login')
    
    if saved_user:
        user = await User.from_phone(saved_user['name'], saved_user['user_phone'])
        print(f"user info refreshed: {user.info()}")
        if user:
            print('user verified in db')
            page.data = {'User': user}
            await page.push_route('/dashboard')
    else:
        print('No saved user')
        await page.push_route('/login')

ft.run(main)