from .objects import events as __events
from .objects import event as __event
from .objects import project_name as __prn

events = __events()

def __setEventType(name):
    global events
    value = f":::{__prn}:{name.upper()}:::"

    setattr(events, name, __event(value))
    events.list.append(name)


__setEventType("MESSAGE_NEW")
__setEventType("MESSAGE_ALLOW")
__setEventType("MESSAGE_DENY")
__setEventType("MESSAGE_EVENT")

__setEventType("PHOTO_NEW")
__setEventType("PHOTO_COMMENT_NEW")
__setEventType("PHOTO_COMMENT_EDIT")
__setEventType("PHOTO_COMMENT_RESTORE")
__setEventType("PHOTO_COMMENT_DELETE")

__setEventType("AUDIO_NEW")

__setEventType("VIDEO_NEW")
__setEventType("VIDEO_COMMENT_NEW")
__setEventType("VIDEO_COMMENT_EDIT")
__setEventType("VIDEO_COMMENT_RESTORE")
__setEventType("VIDEO_COMMENT_DELETE")

__setEventType("WALL_POST_NEW")
__setEventType("WALL_REPOST")
__setEventType("WALL_REPLY_NEW")
__setEventType("WALL_REPLY_EDIT")
__setEventType("WALL_REPLY_RESTORE") 
__setEventType("WALL_REPLY_DELETE") 

__setEventType("BOARD_POST_NEW") 
__setEventType("BOARD_POST_EDIT") 
__setEventType("BOARD_POST_RESTORE") 
__setEventType("BOARD_POST_DELETE") 

__setEventType("MARKET_COMMENT_NEW") 
__setEventType("MARKET_COMMENT_EDIT") 
__setEventType("MARKET_COMMENT_RESTORE") 
__setEventType("MARKET_COMMENT_DELETE") 
__setEventType("MARKET_ORDER_NEW") 
__setEventType("MARKET_ORDER_EDIT")  

__setEventType("GROUP_LEAVE") 
__setEventType("GROUP_JOIN") 

__setEventType("USER_BLOCK") 
__setEventType("USER_UNBLOCK") 

__setEventType("POLL_VOTE_NEW") 

__setEventType("GROUP_OFFICERS_EDIT") 
__setEventType("GROUP_CHANGE_SETTINGS") 
__setEventType("GROUP_CHANGE_PHOTO") 

__setEventType("VKPAY_TRANSACTION") 
__setEventType("APP_PAYLOAD") 

__setEventType("LIKE_ADD") 
__setEventType("LIKE_REMOVE")  