from datetime import datetime
import logging
import sys
import asyncio

from ._get_type import getType
import openhivenpy.exceptions as errs
from openhivenpy.gateway.http import HTTPClient

logger = logging.getLogger(__name__)

__all__ = ['DeletedMessage', 'Message']


class DeletedMessage:
    """`openhivenpy.types.DeletedMessage`
    
    Data Class for a removed Hiven message
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    The class inherits all the available data from Hiven(attr -> read-only)!
    
    Returned with on_message_delete()
    
    Attributes
    ~~~~~~~~~~
    
    house_id: `int` - ID of the House where the message was deleted
    
    message_id: `int` - ID of the message that was deleted
    
    room_id: `int` - ID of the Room where the message was deleted
    
    """
    def __init__(self, data: dict):
        self._message_id = int(data.get('message_id'))
        self._house_id = int(data.get('house_id'))
        self._room_id = int(data.get('room_id'))

    @property
    def message_id(self):
        return int(self._message_id)

    @property
    def house_id(self):
        return int(self._house_id)

    @property
    def room_id(self):
        return int(self._room_id)
    

class Message:
    """`openhivenpy.types.Message`
    
    Data Class for a standard Hiven message
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    The class inherits all the available data from Hiven(attr -> read-only)!
    
    Returned with room message list and House.get_message()
 
    Attributes
    ~~~~~~~~~~
    
    id: `int` - ID of the Message
    
    content: `str` - Simple string content of the message
    
    author: `openhivenpy.types.User` - Author Object
    
    author_id: `int` - ID of the Author that created the message
    
    room: `openhivenpy.types.Room` - Room where the message was sent
    
    room_id: `int` - ID of the Room where the message was deleted
    
    house: `openhivenpy.types.House` - House where the message was sent
    
    house_id: `int` - ID of the House where the message was deleted
    
    created_at: `datetime.datetime` - Creation timestamp
    
    edited_at: `datetime.datetime` - If edited returns a string timestamp else None
    
    attachment: `str` - In work
    
    mentions: `openhivenpy.types.Mention` - A list of Mention objects 
    
    exploding: `None` - In work
    
    """
    def __init__(self, data: dict, http_client: HTTPClient, house, room, author):
        try:
            id = data.get('id', 0)
            self._id = int(id) if data.get('id') is not None else None
            self._author = author
            self._attachment = data.get('attachment')
            self._content = data.get('content')
            
            # Converting to seconds because it's in milliseconds
            if data.get('timestamp') is not None:
                self._timestamp = datetime.fromtimestamp(int(data.get('timestamp')) / 1000) 
            else:
                self._timestamp = None
                
            self._edited_at = data.get('edited_at')
            self._mentions = [getType.mention(data, self._timestamp, self._author, http_client) for data in data.get('mentions', [])]
            self._type = data.get('type') # I believe, 0 = normal message, 1 = system.
            self._exploding = data.get('exploding')
            
            self._house_id = data.get('house_id')
            self._house_id = int(data.get('house_id')) if data.get('house_id') is not None else None
            self._house = house
            self._room_id = int(data.get('room_id')) if data.get('room_id') is not None else None
            self._room = room 
            
            self._embed = getType.embed(data.get('embed')) if data.get('embed') is not None else None

            self._http_client = http_client
            
        except AttributeError as e: 
            logger.error(f"Failed to initialize the Message object! "
                         f"Cause of Error: {sys.exc_info()[1].__class__.__name__}, {str(e)} Data: {data} Data: {data}")
            raise errs.FaultyInitialization(f"Failed to initialize Message object! Possibly faulty data! "
                                            f"Cause of error: {sys.exc_info()[1].__class__.__name__}, {str(e)}")
        
        except Exception as e: 
            logger.error(f"Failed to initialize the Message object! "
                         f"Cause of Error: {sys.exc_info()[1].__class__.__name__}, {str(e)} Data: {data}")
            raise errs.FaultyInitialization(f"Failed to initialize Message object! Possibly faulty data! "
                                            f"Cause of error: {sys.exc_info()[1].__class__.__name__}, {str(e)}")

    @property
    def id(self):
        return int(self._id)

    @property
    def author(self):
        return self._author

    @property
    def created_at(self):
        return self._timestamp

    @property
    def edited_at(self):
        return self._edited_at

    @property
    def room(self):
        return self._room

    @property
    def house(self):
        return self._house

    @property
    def attachment(self):
        return self._attachment

    @property
    def content(self):
        return self._content

    @property
    def mentions(self):
        return self._mentions

    @property
    def room_id(self):
        return self._room_id

    @property
    def house_id(self):
        return self._house_id

    @property 
    def embed(self):
        return self._embed

    async def mark_message_as_read(self, delay: float) -> bool:
        """`openhivenpy.types.Message.ack`

        Marks the message as read. This doesn't need to be done for bot clients. 
        
        Returns `True` if successful.
        
        Parameter
        ~~~~~~~~~
        
        delay: `float` - Delay until marking the message as read (in seconds)
        
        """
        http_code = "Unknown"
        try:
            resp = await self._http_client.post(endpoint=f"/rooms/{self.room_id}/messages/{self.id}/ack")
            if resp:
                http_code = resp.status
            else:
                raise errs.HTTPFaultyResponse
            await asyncio.sleep(delay=delay)
            return True
        
        except Exception as e:
            logger.error(f"Failed to mark the message in room {self.room.name} with id {self.id} as marked." 
                         "[CODE={http_code}] Cause of Error: {sys.exc_info()[1].__class__.__name__}, {str(e)}")

    async def delete(self, delay: float) -> bool:
        """`openhivenpy.types.Message.delete()`

        Deletes the message. Raises Forbidden if not allowed. 
        
        Returns a `DeletedMessage` Object if successful
        
        Parameter
        ~~~~~~~~~
        
        delay: `float` - Delay until deleting the message as read (in seconds)
        
        """
        http_code = "Unknown"
        try:
            await asyncio.sleep(delay=delay)
            
            resp = await self._http_client.delete(endpoint=f"/rooms/{self.room_id}/messages/{self.id}")
            if resp:
                http_code = resp.status
            else:
                raise errs.HTTPFaultyResponse
            
            if http_code < 300:
                return True
            else:
                return False
        
        except Exception as e:
            logger.error(f"Failed to delete the message in room {self.room.name} with id {self.id}." 
                         f"[CODE={http_code}] Cause of Error: {sys.exc_info()[1].__class__.__name__}, {str(e)}")

    async def edit(self, content: str) -> bool:
        """`openhivenpy.types.House.edit()`

        Edits a message on Hiven
            
        Returns 'True' if successful.

        """
        http_code = "Unknown"
        try:
            resp = await self._http_client.patch(endpoint=f"/rooms/{self.room_id}/messages/{self.id}",
                                                     json= {'content': content})
            if resp:
                http_code = resp.status
            else:
                raise errs.HTTPFaultyResponse
            
            return True
    
        except Exception as e:
            logger.error(f"Failed to edit messsage in room {self.room.name} with id {self.id}." 
                         f"[CODE={http_code}] Cause of Error: {sys.exc_info()[1].__class__.__name__}, {str(e)}")
            return False
