from channels.db import database_sync_to_async

from .exceptions import ClientError
from .models import Rooms

@database_sync_to_async
def get_room_or_error(room_id, user):
   
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    try:
        room = Rooms.objects.get(RoomID=room_id)
    except Rooms.DoesNotExist:
        raise ClientError("ROOM_INVALID")
    
    return room