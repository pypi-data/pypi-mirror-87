import sys
import logging
import datetime
import asyncio
import time
from typing import Union

from ._get_type import getType
import openhivenpy.exceptions as errs

logger = logging.getLogger(__name__)

__all__ = ['Client']


class Client:
    """`openhivenpy.types.Client` 
    
    Date Class for a Client
    ~~~~~~~~~~~~~~~~~~~~~~~
    
    Data Class that stores the data of the connected client
    
    """
    async def update_client_user_data(self, data: dict = None) -> None:
        """`openhivenpy.types.client.update_client_user_data()`
         
        Updates or creates the standard user data attributes of the Client
        
        """
        try: 
            # Using a USER object to actually store all user data
            self._USER = await getType.a_user(data, self.http_client)
            relationships = data.get('relationships', [])
            for key in relationships:
                self._relationships.append(await getType.a_relationship(relationships.get(key, {}), self.http_client))
                
            private_rooms = data.get('private_rooms', [])
            for private_room in private_rooms:
                type = int(private_room.get('type', 0))
                if type == 1:
                    room = await getType.a_private_room(private_room, self.http_client)
                elif type == 2:
                    room = await getType.a_private_group_room(private_room, self.http_client)
                else:
                    room = await getType.a_private_room(private_room, self.http_client)
                self._private_rooms.append(room)
            
            houses_ids = data.get('house_memberships', [])
            self._amount_houses = len(houses_ids)
                        
        except AttributeError as e: 
            logger.error(f"FAILED to update client data! " 
                         f"Cause of Error: {sys.exc_info()[1].__class__.__name__}, {str(e)}")
            raise AttributeError(f"FAILED to update client data! Most likely faulty data!" 
                                 f"Cause of error: {sys.exc_info()[1].__class__.__name__}, {str(e)}")
        except KeyError as e:
            logger.error(f"FAILED to update client data! " 
                         f"Cause of Error: {sys.exc_info()[1].__class__.__name__}, {str(e)}")
            raise AttributeError(f"FAILED to update client data! Most likely faulty data! " 
                                 f"Cause of error: {sys.exc_info()[1].__class__.__name__}, {str(e)}")
        except Exception as e:
            logger.error(f"FAILED to update client data! "
                         f"Cause of Error: {sys.exc_info()[1].__class__.__name__}, {str(e)}")
            raise errs.FaultyInitialization(f"FAILED to update client data! Possibly faulty data! " 
                                            f"Cause of error: {sys.exc_info()[1].__class__.__name__}, {str(e)}")

    def __init__(self, *, http_client = None, **kwargs):
        self.http_client = http_client if http_client is not None else self.http_client

        self._amount_houses = 0
        self._houses = []
        self._users = []
        self._rooms = []
        self._private_rooms = []
        self._relationships = []
        self._USER = getType.user(data=kwargs, http_client=self.http_client)

        # Init Data that will be overwritten by the connection and websocket
        self._initialized = False
        self._connection_start = None
        self._startup_time = None
        self._ready = False

        self._event_handler = None if not hasattr(self, '_event_handler') else self._event_handler
        self._execution_loop = None if not hasattr(self, '_execution_loop') else self._execution_loop

        # Appends the ready check function to the execution_loop
        self._execution_loop.create_one_time_task(self.check_meta_data)

    async def check_meta_data(self):
        """
        Checks whether the meta data is complete and triggers on_ready
        """
        while True:
            if self._amount_houses == len(self._houses) and self._initialized:
                self._startup_time = time.time() - self.connection_start
                self._ready = True
                await self._event_handler.ready_state()
                break
            elif (time.time() - self.connection_start) > 20 and len(self._houses) >= 1:
                self._ready = True
                await self._event_handler.ready_state()
                break
            await asyncio.sleep(0.5)

    async def edit(self, **kwargs) -> bool:
        """`openhivenpy.types.Client.edit()`
        
        Change the signed in user's/bot's data. 
        
        Available options: header, icon, bio, location, website
        
        Returns `True` if successful
        
        """
        http_code = "Unknown"
        try:
            for key in kwargs.keys():
                if key in ['header', 'icon', 'bio', 'location', 'website']:
                    response = await self.http_client.patch(endpoint="/users/@me", data={key: kwargs.get(key)})
                    http_code = response.status
                    return True
                else:
                    logger.error("The passed value does not exist in the user context!")
                    raise KeyError("The passed value does not exist in the user context!")
    
        except Exception as e:
            keys = "".join(str(" "+key) for key in kwargs.keys())
            logger.error(f"Failed change the values {keys} on the client Account! [CODE={http_code}] "
                         f"Cause of Error: {sys.exc_info()[1].__class__.__name__}, {str(e)}")
            raise errs.HTTPError(f"Failed change the values {keys} on the client Account!")    

    @property
    def amount_houses(self) -> int:
        return self._amount_houses

    @property
    def relationships(self) -> list:
        return self._relationships

    @property
    def private_rooms(self) -> list:
        return self._private_rooms
    
    @property
    def username(self) -> str:
        return self._USER.username

    @property
    def name(self) -> str:
        return self._USER.name

    @property
    def id(self) -> int:
        return int(self._USER.id)

    @property
    def icon(self) -> str:
        return self._USER._icon
    
    @property
    def header(self) -> str:
        return self._USER._header

    @property
    def bot(self) -> bool:
        return self._USER.bot

    @property
    def location(self) -> str:
        return self._USER.location

    @property
    def website(self) -> str:
        return self._USER.website

    @property
    def presence(self) -> getType.presence:
        return self._USER.presence

    @property
    def joined_at(self) -> Union[datetime.datetime, None]:
        if self._USER._joined_at is not None and self._USER._joined_at != "":
            return datetime.datetime.fromisoformat(self._USER._joined_at[:10])
        else:
            return None
