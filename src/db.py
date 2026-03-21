from supabase import create_client , acreate_client

URL = 'https://ltmyyctdzbibbfpughdt.supabase.co'
KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx0bXl5Y3RkemJpYmJmcHVnaGR0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE4NTQxNTksImV4cCI6MjA4NzQzMDE1OX0.TaJLUSwm-PwrfeZ8pG25OXIgRLNFFiiJU87J1wF7noI'

supabase = create_client(URL, KEY)

# async client for realtime
async def get_async_client():
    return await acreate_client(URL, KEY)