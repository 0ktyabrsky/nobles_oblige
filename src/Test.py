import flet as ft
from servises import user as us

# windows screen settings 
MOBILE_WIDTH = 380
def mobile_wrapper(content):
    return ft.Row(
        alignment = ft.MainAxisAlignment.CENTER,
        controls= [
            ft.Container(
                width = MOBILE_WIDTH,
                padding = 16,
                content = content
            )
        ]
    )


test_user = us.User(user_id = '996888',user_name = 'Lola')




