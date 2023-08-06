from datetime import datetime

from . import _databases
from . import objects
from .tools import assets
import asyncio
import random


expressions = objects.expressions()
expressions.id = 0

def setExpression(name, value = None):
    global expressions
    if value == None: value = f":::{objects.project_name}:{name}:::"
        
    setattr(expressions, name, objects.expression(value))
    expressions.list.append(name)


setExpression("LOGGER_START", [
    'TESTCANARYBOT 0.8',
    'KENSOI.GITHUB.IO 2020', ''
])
setExpression("SESSION_START", "started")
setExpression("SESSION_LONGPOLL_START", "connected")
setExpression("SESSION_LONGPOLL_ERROR", "is not connected [LongpollError Exception]")
setExpression("SESSION_CLOSE", "session closed")
setExpression("SESSION_LISTEN_START", "listenning is started")
setExpression("SESSION_LISTEN_CLOSE", "listenning is finished")

setExpression("MESSAGE_HANDLER_ITEMS", "\t\titems: {items}")
setExpression("MESSAGE_HANDLER_TYPE", "{event_type}")
setExpression("MESSAGE_HANDLER_CHAT", "\t\tchat: {peer_id}")
setExpression("MESSAGE_HANDLER_USER", "\t\tuser: {from_id}")

setExpression("ENDLINE")
setExpression("ASSETS_ERROR")

setExpression("MENTION")
setExpression("ACTION")
setExpression("PAYLOAD")

setExpression("NOREACT")
setExpression("PARSER")
setExpression("LIBRARY")
setExpression("LIBRARY_ERROR")
setExpression("LIBRARY_NOSELECT")
setExpression("LIBRARY_PIC")

setExpression("LIBRARY_RESPONSE_ERROR")
setExpression("LIBRARY_RESPONSE_LIST")
setExpression("LIBRARY_RESPONSE_LIST_LINE", "{listitem} {codename} - {name}")
setExpression("LIBRARY_RESPONSE_LIST_ITEM", "\u2022")
setExpression("LIBRARY_RESPONSE_DESCR", "{name}: \n{descr} ")

setExpression("FWD_MES", "forwarded messages")
setExpression("BEEPA_PAPASA", ":::NYASHKA:NYASHKA:::")

setExpression("PLUGIN_INIT", "{} is loading")
setExpression("PLUGIN_FAILED_BROKEN", "loading error: broken {}")
setExpression("PLUGIN_FAILED_ATTRIBUTES", "loading error: check for \"name\", \"description\" and \"version\" attributes")
setExpression("PLUGIN_FAILED_PACKAGETYPE", "loading error: plugin has \"package_handler\" coroutine, but does not have attribute \"packagetype\"")
setExpression("PLUGIN_FAILED_HANDLERS", "loading does not have any handlers. \n\t\tYou can put one of these functions:\n\t\tasync def error_handler(self, tools, package)\n\t\tasync def package_handler(self, tools, package)")

setExpression("MENTIONS", list())
setExpression("MENTION_NAME_CASES", list())
setExpression("NOT_COMMAND")


setExpression("ONLY_COMMANDS", True)
setExpression("CHAIN_CM", [])


class tools:
    def __init__(self, number, api, http):
        self.__db = _databases.Databases(("system", "system.db"))
        self.get = self.__db.get

        self.plugin = "system"
        self.log = assets("log.txt", "a+", encoding="utf-8")

        self.group_id = number
        self.api = api
        self.http = http
        asyncio.get_event_loop().run_until_complete(self.__setShort())

        self.group_mention = f'[club{self.group_id}|@{self.group_address}]'
        self.mentions = [self.group_mention]
        self.mentions_name_cases = []


        for print_test in self.getValue("LOGGER_START").value:
            print(print_test, 
                file = self.log
                )
                
        self.log.flush()

        self.name_cases = [
            'nom', 'gen', 
            'dat', 'acc', 
            'ins', 'abl'
            ]
        self.mentions_self = {
            'nom': 'я', 
            'gen': ['меня', 'себя'],
            'dat': ['мне', 'себе'],
            'acc': ['меня', 'себя'],
            'ins': ['мной', 'собой'],
            'abl': ['мне','себе'],
        }
        self.mentions_unknown = {
            'all': 'всех',
            'him': 'его',
            'her': 'её',
            'it': 'это',
            'they': 'их',
            'them': 'их',
            'us': 'нас',
            'everyone': ['@everyone', '@all', '@все']
        }

    
    async def __setShort(self):
        res = await self.api.groups.getById(group_id=self.group_id)
        self.group_address = res[0].screen_name


    def system_message(self, textToPrint:str):
        response = f'@{self.group_address}.{self.plugin}: {textToPrint}'

        print(response)
        print(f"{self.getDateTime()} {response}", file=self.log)

        self.log.flush()


    def random_id(self):
        return random.randint(0, 99999999)


    def ischecktype(self, checklist, checktype):
        for i in checklist:
            if isinstance(checktype, list) and type(i) in checktype:
                return True
                
            elif isinstance(checktype, type) and isinstance(i, checktype): 
                return True
            
        return False


    def getDate(self, time = datetime.now()):
        return f'{"%02d" % time.day}.{"%02d" % time.month}.{time.year}'
    
    
    def getTime(self, time = datetime.now()):
        return f'{"%02d" % time.hour}:{"%02d" % time.minute}:{"%02d" % time.second}'


    def getDateTime(self, time = datetime.now()):
        return self.getDate(time) + ' ' + self.getTime(time)


    def setValue(self, nameOfObject: str, newValue):
        setExpression(nameOfObject, newValue)
        self.update_list()


    def getValue(self, nameOfObject: str):
        try:
            return getattr(expressions, nameOfObject)
            
        except AttributeError as e:
            return "AttributeError"


    def update_list(self):
        if hasattr(self, "expression_list"):
            if expressions.list != self.expression_list:
                self.expression_list = expressions.list
        
        else:
            self.expression_list = expressions.list



    def add(self, db_name):
        self.__db.add((db_name, self.assets.path + db_name))


    async def getMention(self, page_id: int, name_case = "nom"):
        if name_case == 'link':
            if page_id > 0:
                return f'[id{page_id}|@id{page_id}]'

            elif page_id == self.group_id:
                return self.group_mention

            else:
                test = await self.api.groups.getById(group_id = -page_id)
                return f'[club{-page_id}|@{test[0].screen_name}]'
        
        else:
            if page_id > 0:
                request = await self.api.users.get(
                    user_ids = page_id, 
                    name_case = name_case
                    )
                first_name = request[0].first_name
                
                return f'[id{page_id}|{first_name}]'
            
            elif page_id == self.group_id:
                return self.selfmention[name_case]
            
            else:
                request = await self.api.groups.getById(
                    group_id = -page_id
                    )
                name = request[0].name
                
                return f'[club{-page_id}|{name}]' 


    async def getManagers(self, group_id = None):
        if not group_id:
            group_id = self.group_id

        elif not isinstance(group_id, int):
            raise TypeError('Group ID should be integer')

        lis = await self.api.groups.getMembers(group_id = group_id, sort = 'id_asc', filter='managers')
        return [i.id for i in lis.items if i.role in ['administrator', 'creator']]


    async def isManager(self, from_id: int, group_id = None):
        if not group_id:
            group_id = self.group_id
            
        elif not isinstance(group_id, int):
            raise TypeError('Group ID should be integer')

        return from_id in await self.getManagers(group_id)


    async def getChatManagers(self, peer_id: int):
        res = await self.api.messages.getConversationsById(peer_ids = peer_id)
        res = res.items[0].chat_settings
        response = [*res.admin_ids, res.owner_id]
        return response
        

    def isChatManager(self, from_id, peer_id: int):
        return from_id in self.getChatManagers(peer_id)


    async def getMembers(self, peer_id: int):
        response = await self.api.messages.getConversationMembers(peer_id = peer_id)
        return [i['member_id'] for i in response['items']]


    async def isMember(self, from_id: int, peer_id: int):
        return from_id in await self.getMembers(peer_id)


    def parse_mention(self, mention):
        response = mention.replace(mention[mention.find('|'):], '')

        response = response.replace('id', '')
        response = response.replace('club', '-')
        response = response.replace('public', '-')
            
        return objects.mention(int(response))


    def parse_link(self, link):
        response = link

        response.replace('https://', '')
        response.replace('http://', '')
        
        return response
