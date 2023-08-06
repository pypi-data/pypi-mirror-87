project_name = "TESTCANARYBOT"


class static:
    pass
    
    
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


class message(Object):
    id = 0
    date = 0
    random_id = 0
    peer_id = 1
    from_id = 1
    items = []


class package(message):
    pass



class expressions:
    list = []


class expression:
    __slots__ = ('value') 
    def __init__(self, variable):
        self.value = variable

    def __str__(self):
        return self.value


class mention:
    __slots__ = ('id') 
    def __init__(self, page_id):
        self.id = page_id

    def __int__(self):
        return self.id


class objectPlugin:
    codename = str()
    name = str()
    version = static
    description = str()
    packagetype = []


class staticPlugin(objectPlugin):
    async def package_handler(self, tools, package):
        pass


    async def error_handler(self, tools, package):
        pass


    async def command_handler(self, tools, package):
        pass