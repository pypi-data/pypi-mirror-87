import logging

from ._get_type import getType
import openhivenpy.exceptions as errs
from openhivenpy.gateway.http import HTTPClient

logger = logging.getLogger(__name__)

__all__ = ['Embed']

class Embed:
    """`openhivenpy.types.Embed`
    
    Data Class for a Embed Object
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    The class inherits all the available data from Hiven(attr -> read-only)!
    
    Returned with a message object if an embed object is added
    
    Attributes
    ~~~~~~~~~~
    
    url: `str` - Endpoint of the embed object
    
    type: `str` - Type of the embed message
    
    title: `str` - Title that displays on the embed object
    
    image: `dict or str` - Url for the image (Currently not in correct format)
                           or dict with data for a video file
    
    description: `str` - Description of the embed object
    
    """
    def __init__(self, data: dict):
        self._url = data.get('url')
        self._type = data.get('type')
        self._title = data.get('title')
        self._image = data.get('image')
        self._description = data.get('description')
        
    @property
    def url(self):
        return self._url
    
    @property
    def type(self):
        return self._type
    
    @property 
    def title(self):
        return self._title

    @property 
    def image(self):
        return self._image
    
    @property
    def description(self):
        return self._description        
