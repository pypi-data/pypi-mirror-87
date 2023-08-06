import os

project_name = "TESTCANARYBOT"


def init_async(coroutine: asyncio.coroutine):
    return asyncio.get_event_loop().run_until_complete(coroutine)

    
class Object:
    def __init__(self, **entries):
        self.__dict__.update(entries)

        for i in self.__dict__.keys():
            attr = getattr(self, i)
            attr_type = type(attr)

            if attr_type == dict:
                setattr(self, i, Object(**attr))

            elif attr_type == list:
                setattr(self, i, [
                    Object(**attr_key) if isinstance(attr_key, dict) else attr_key for attr_key in attr
                    ])


class static:
    pass


class events:
    def __init__(self):
        self.list = []


class event:
    __slots__ = ('value') 
    def __init__(self, variable):
        self.value = variable


class expressions:
    def __init__(self):
        self.list = []


class expression:
    __slots__ = ('value') 
    def __init__(self, variable):
        self.value = variable

    def __str__(self):
        return self.value


class mention:
    def __init__(self, page_id):
        self.id = page_id

    def __int__(self):
        return self.id


class message(Object):
    id = 0
    date = 0
    random_id = 0
    peer_id = 1
    from_id = 1
    attachments = []
    payload = ''
    keyboard = {}
    fwd_messages = []
    reply_message = {}
    action = {}
    conversation_message_id = ''
    type = event('empty')
    items = []
    text = ''


class package(message):
    pass


class staticPlugin:
    name = ""
    version = static
    description = "whatever"
    packagetype = []

    async def package_handler(self, tools, package):
        pass


    async def error_handler(self, tools, package):
        pass


    async def command_handler(self, tools, package):
        pass