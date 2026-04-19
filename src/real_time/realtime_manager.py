
import websockets
import json
from db import KEY, PROJECT_ID
import asyncio




# With Supabase
SUPABASE_WS_URL = f"wss://{PROJECT_ID}.supabase.co/realtime/v1/websocket?apikey={KEY}"

# realtime manager so i can dinamaclly show to user it's groups and dms without polling every time
'''
functions:
create a web socket
subsribe to the exact table : group members and messages 
activate when only NEW row will be in there and ONLY when user_id match with user so it wont show groups wherer user is not presented
and show messages only in specific groups
newly data will be send back to the server
Listen to those new data 
adding them to the new_groups and new_messages values so i can use them
'''
class RealtimeManager:
    def __init__(self):
        self.ws = None
        self.on_new_group = None
        self.on_new_message = None
        self.on_delete_group = None
    # connects to websocket and automatically geting callbacks from it
    async def connect_groups(self, user_id: str):
        while True:
            try:


                self.ws = await websockets.connect(SUPABASE_WS_URL) # start connecting 
                await self._subscribe_groups(user_id)   # checking for new group and adding it call backs
            
                await self._listen() # automatically getting this data from call backs and cheking constantly
            except Exception as e:
                print('WS ERROR:', e)
                await asyncio.sleep(2)
    
    
    async def connect_messages(self, group_id: str):
        await self._subscribe_messages(group_id) # checking for new messages too
    async def switch_chats(self, new_group_id: str):
        await self._subscribe_messages(new_group_id) # if user change group check messages from this group only
    # subscribing for group changes: broadcasting for any new groups added . even id someone added me
    async def _subscribe_groups(self, user_id:str):
        await self.ws.send(json.dumps({
            'event': 'phx_join',
            'topic' : 'realtime:public:group_members',
            'payload': {
                 'config' : {
                     'postgres_changes' : [
                         {'event' : 'INSERT',
                          'schema' :'public',
                          'table' : 'group_members',
                          'filter' : f'user_id=eq.{user_id}'
                          },
                          {
                            'event' : 'DELETE',
                            'schema' : 'public',
                            'table' : 'group_members',
                            'filter' : f'user_id=eq.{user_id}'
                          }
                     ],
                     'broadcast' :{ 'self': True}
                     }
                },
            'ref' : '1'
        }))
    # subscribing fro any message changes 
    async def _subscribe_messages(self, group_id: str):
        await self.ws.send(json.dumps({
            'event': 'phx_join',
            'topic': f"realtime:public:messages:group_id=eq.{group_id}",
            'payload' : {},
            'ref' : '2'
        }))
    # listening (taking the data back) to the ws value 

    async def _listen(self):
        async for raw in self.ws:
            print(f"Realtime Raw: {raw}")
            event = json.loads(raw)
            if event.get('event') != 'postgres_changes':
                continue
            topic = event.get('topic', '')
            payload = event.get('payload', {})
            data = payload.get('data', {})
            print(
                f'Raw data: {data}'
            )

            record = data.get('record')
            old_record = data.get('old_record')
            event_type = data.get('type')



            if not record and not old_record:
                continue

        # if in payload there is topic group add it to the variable
            if 'group_members' in topic:

                # loking for specific events ( delete , inserte etc)
                
                if event_type == 'INSERT' and record:
                    if self.on_new_group:
                        await self.on_new_group(record)
                
                if event_type == 'DELETE' and old_record:
                    if self.on_delete_group:
                        await self.on_delete_group(old_record)

        # if in payload there is topic message add it to the variable
            if 'messages' in topic:
                if self.on_new_message:
                    await self.on_new_message(record)
    
    # disconecting realtime
    async def dissconect(self):
        if self.ws:
            await self.ws.close()

# single instance used across all pages
realtime_manager = RealtimeManager()

            

