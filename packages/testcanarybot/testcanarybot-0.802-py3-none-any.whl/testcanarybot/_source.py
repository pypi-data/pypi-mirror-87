from . import exceptions
from . import objects
from ._values import events
from ._values import expressions
from ._values import setExpression

from datetime import datetime

import aiohttp
import atexit
import asyncio
import importlib
import json
import os
import random
import sqlite3
import time
import traceback
import six

loop = asyncio.get_event_loop()

class _assets:
    def __init__(self):
        self.path = os.getcwd() + '\\assets\\'

    def __call__(self, *args, **kwargs):
        args = list(args)
        if len(args) > 0:
            args[0] = self.path + args[0]
        
        elif 'file' in kwargs:
            kwargs['file'] = self.path + kwargs['file']
        
        return open(*args, **kwargs)

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class _ohr:
    from_id = ['deleter_id', 'liker_id', 'user_id']
    peer_id = ['market_owner_id', 'owner_id', 'object_owner_id', 
                'post_owner_id', 'photo_owner_id', 'topic_owner_id', 
                'video_owner_id', 'to_id'
                ]


class api:
    __slots__ = ('_http', '_method', '_string')

    def __init__(self, __http, method, string = None):
        self._http = __http
        self._method = method    
        self._string = string


    def __getattr__(self, method):
        if '_' in method:
            m = method.split('_')
            method = m[0] + ''.join(i.title() for i in m[1:])

        self._string = self._string + "." if self._string else ""

        return api(
            self._http, self._method,
            (self._string if self._method else '') + method
        )

    async def __call__(self, **kwargs):
        for k, v in six.iteritems(kwargs):
            if isinstance(v, (list, tuple)):
                kwargs[k] = ','.join(str(x) for x in v)

        result = await self._method(self._string, kwargs)
        if isinstance(result, list):
            return [
                objects.Object(**i) for i in result
            ]
        
        elif isinstance(result, dict):
            return objects.Object(**result)

        else:
            return result


class app:    
    __RPS_DELAY = 1 / 20.0
    headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) '
                            'Gecko/20100101 Firefox/52.0'
        }

    def __init__(self, token: str, group_id: int, api_version='5.126'):
        """
        Token = token you took from VK Settings: https://vk.com/{yourgroupaddress}?act=tokens
        group_id = identificator of your group where you want to install CanaryBot Framework :)
        """
        
        for filename in ['\\assets\\', '\\library\\']:
            try:
                os.mkdir(os.getcwd() + filename)
            except:
                pass
        
        self.last_request = 0.0

        self.__token = token
        self.__group_id = group_id
        self.api_version = api_version

        self.longpoll = None
        self.__http = aiohttp.ClientSession()
        self.api = api(self.__http, self.method)
        self.__library = library(supporting, group_id, self.api, self.__http)
        
        
        self.atexit = atexit
        self.atexit.register(self.__close_session)

        text = self.__library.tools.getValue('SESSION_START').value
        print(f"\n@{self.__library.tools.group_address}: {text}")
        print(f"\n{self.__library.tools.getDateTime()} @{self.__library.tools.group_address}: {text}", file=self.__library.tools.log)
        


    def __close_session(self):
        loop.run_until_complete(self.__http.close())
        self.__library.tools.plugin = "http"
        self.__library.tools.system_message(self.__library.tools.getValue("SESSION_CLOSE").value)
        self.__library.tools.log.close()


    async def get(self, *args, **kwargs):
        self.__http.get(*args, **kwargs)


    async def post(self, *args, **kwargs):
        self.__http.post(*args, **kwargs)


    async def method(self, method: str, values=None):
        """ Вызов метода API

        :param method: название метода
        :type method: str

        :param values: параметры
        :type values: dict
        """
        data = values if values else dict()

        data['v'] = self.api_version

        data['access_token'] = self.__token
        if 'group_id' in data: data['group_id'] = self.__group_id

        delay = self.__RPS_DELAY - (time.time() - self.last_request)

        if delay > 0:
            await asyncio.sleep(delay)

        response = await self.__http.post(
            'https://api.vk.com/method/' + method, 
            data = data, 
            headers = self.headers
        )

        self.last_request = time.time()

        response = await response.json()
        if 'error' in response:
            
            raise TypeError(f"[{response['error']['error_code']}] {response['error']['error_msg']}")

        return response['response']    


    def setMentions(self, *args):
        """
        Use custom mentions instead "@{groupadress}"
        """
        self.__library.tools.setValue("MENTIONS", [self.__library.tools.group_mention, *[str(i).lower() for i in args]])


    def setNameCases(self, *args):
        """Use custom mentions instead \"@{groupaddress}\""""
        self.__library.tools.setValue("MENTION_NAME_CASES", args)


    def getModule(self, name: str):
        return self.__library.plugins[name]


    def getTools(self):
        return self.__library.tools


    def getValue(self, string: str):
        self.__library.tools.getValue(string)
    

    def setValue(self, string: str, value):
        self.__library.tools.setValue(string, value)


    def listen(self, count = None):
        """count: how many packages should take Canarybot. If you don't send this, it takes packages forever"""
        self.__library.tools.system_message(self.__library.tools.getValue("SESSION_LISTEN_START").value)
        if not count:
            while True:
                self.check()

        else:
            for i in range(count):
                self.check()

            self.__library.tools.system_message(self.__library.tools.getValue("SESSION_LISTEN_CLOSE").value)


    def getTools(self):
        return self.__library.tools

    def install(self):
        """set up framework to work with 'library' folder"""

        self.__library.upload()
        self.modules_list = list(self.__library.plugins.keys())
        self.longpoll = longpoll(self.__http, self.method, self.__group_id)
        self.__library.tools.system_message(self.__library.tools.getValue("SESSION_LONGPOLL_START").value)


    def hide(self, *args):
        self.__library.hidelist = args


    def check(self):
        """Check VK for updates once time, like canarybot.listen(1)"""
        self.__library.tools.update_list()

        if not self.longpoll:
            raise exceptions.LongpollError(self.__library.tools.getValue("SESSION_LONGPOLL_ERROR"))

        if not self.__library.plugins:
            raise exceptions.LibraryError(self.__library.tools.getValue("SESSION_LIBRARY_ERROR"))

        response = loop.run_until_complete(self.longpoll.check())

        for event in response:
            self.__library.send(event)


class Database:
    def __init__(self, directory):
        self.directory = 'assets/' + directory
        self.connection = sqlite3.connect(self.directory)
        self.cursor = self.connection.cursor()


    def request(self, request: str):
        self.cursor.execute(request)
        self.connection.commit()
        
        return self.cursor.fetchall()


    def close(self):
        self.connection.close()


class Databases:
    def __init__(self, names: list):
        self.upload(names)


    def check(self, name):
        response = [*self.__dbs.keys(), 
                *[i.directory for i in self.__dbs.values()]]

        return name in response 


    def upload(self, names):
        self.__dbs = {}
        self.add(names)


    def get(self, name):
        check = type(name)
        if check == tuple:
            if not self.check(name[0]):
                raise exceptions.DBError("This DB does not exist")

            else:
                return self.__dbs[name[1]]

        elif check == str:
            if not self.check(name):
                raise exceptions.DBError("This DB does not exist")

            else:
                return self.__dbs[name]



    def add(self, names): 
        check = type(names)

        if check == list:
            for name in names:
                if self.check(name[0]):
                    raise DBError("This DB already exists")

                else:
                    self.__dbs[name[0]] = Database(name[1])

        elif check == tuple:
            if self.check(names[0]):
                raise DBError("This DB already exists")

            else:
                self.__dbs[names[0]] = Database(names[1])

        elif check == str:
            if self.check(names):
                raise DBError("This DB already exists")

            else:
                self.__dbs[names] = Database(names)
        
        else:
            raise DBError("Incorrect type of 'names'")


class library:
    def __init__(self, v, group_id, api, http):
        path = os.getcwd()
        self.tools = tools(group_id, api, http)
        self.hidelist = []

        self.error_handlers = ['static']
        self.package_handlers = self.error_handlers.copy()
        self.command_handlers = self.error_handlers.copy()

        self.defattr = {
            "error_handler", 
            "package_handler", 
            "command_handler"
            }

        self.needattr = {
            'name',
            'version',
            'description',
        }
        self.supp_v = v


    def upload(self):
        self.plugins = dict()
        self.tools.plugin = "library"
        response = list()

        try:
            response.extend(os.listdir(os.getcwd() + '\\library\\'))
            
        except Exception as e:
            self.tools.system_message(e)
        
        for name in ['sampleplugin', '__pycache__']:
            if name in response: response.remove(name)
        response.append('static')

        loop.run_until_complete(asyncio.gather(*[
                                self.pluginload(plugin) for plugin in response
                                ]))



    async def pluginload(self, plugin):
        if plugin != 'static':
            self.tools.system_message(self.tools.getValue("PLUGIN_INIT").value.format(plugin))
            try:
                if plugin.endswith('.py'):
                    pluginObj = getattr(
                        importlib.import_module("library." + plugin[:-3]),
                        "Main")()
                else:
                    pluginObj = getattr(
                        importlib.import_module("library." + plugin + ".main"),
                        "Main")()
                await pluginObj.start(self.tools)

            except Exception as e:
                self.tools.system_message(self.tools.getValue("PLUGIN_FAILED_BROKEN").value.format(e))

                return None
            
            attributes = set(dir(pluginObj))
            if self.needattr & attributes != self.needattr:
                self.tools.system_message(self.tools.getValue("PLUGIN_FAILED_ATTRIBUTES").value)

                return None


            if self.defattr & attributes != {}:
                if plugin.endswith(".py"): plugin = plugin.replace(".py", "")

                if 'package_handler' in attributes:
                    if hasattr(pluginObj, "packagetype"):
                        self.package_handlers.append(plugin)

                    else:
                        self.tools.system_message(self.tools.getValue("PLUGIN_FAILED_PACKAGETYPE").value)

                if 'command_handler' in attributes:
                    self.command_handlers.append(plugin)

                if 'error_handler' in attributes:
                    self.error_handlers.append(plugin)
                    
                self.plugins[plugin] = pluginObj

            else:
                self.tools.system_message(self.tools.getValue("PLUGIN_FAILED_HANDLERS").value)
        else:
            pluginObj = objects.staticPlugin()
            self.plugins[plugin] = pluginObj


    def send(self, event):
        if hasattr(events, event['type']):
            event_type = getattr(events, event['type'])
            if event_type == events.message_new:
                self.parse(
                    objects.message(**event['object']['message'])
                )

            else:
                self.parse_package(
                    self.object_handler(event_type, event['object'])
                )


    def object_handler(self, event_type, event_object):
        package_handled = objects.package
        package_handled.peer_id = event_object['user_id']

        for key, value in obj.items():
            if key in _ohr.peer_id: 
                package_handled.peer_id = value

            if key in _ohr.from_id: 
                package_handled.from_id = value

            package_handled[key] = value
        
        package_handled.items.append(event)
        package_handled.items.append(self.tools.getObject("ENDLINE"))
        package_handled.type = event_type
        package_handled.__dict__.update(
            event_object
        )

        return package_handled


    def parse(self, message):
        message.type = events.message_new
        message.items = []

        if hasattr(message, 'action'):
            message.items = [self.tools.getValue("ACTION")]

        elif hasattr(message, 'payload'):
            message.items = [self.tools.getValue("PAYLOAD")]
            message.payload = json.loads(message.payload)

        elif hasattr(message, 'text') and message.text != '': 
            message.items = self.parse_command(message.text)
            
        message.items.append(self.tools.getValue("ENDLINE"))
        if len(event_package.items) != 0 or not self.tools.getValue("ONLY_COMMANDS").value:
            self.parse_package(message)


    def parse_command(self, messagetoreact):
        for i in self.tools.expression_list:
            value = self.tools.getValue(i)

            if type(value) is str and value in messagetoreact:
                messagetoreact = messagetoreact.replace(i, ':::SYSTEM:::')

        response = []
        message = messagetoreact.split() 

        if len(message) > 1:
            if message[0] in [*self.tools.getValue("MENTIONS").value]:
                message.pop(0)

                for i in message:
                    if i[0] == '[' and i[-1] == ']' and i.count('|') == 1:
                        response.append(self.tools.parse_mention(i[1:-1]))

                    else:
                        response.append(self.tools.parse_link(i))

            if len(response) != 0:
                return response
        
        if self.tools.getValue("ADD_MENTIONS").value:
            for word in message:
                if word.lower() in [*self.tools.getValue("MENTIONS").value, 
                                    *self.tools.getValue("MENTION_NAME_CASES").value]: 
                    response.append(self.tools.getValue("MENTION"))

            if len(response) != 0:
                return response

        if not self.tools.getValue("ONLY_COMMANDS").value:
            response.append(self.tools.getValue("NOT_COMMAND"))
            return response

        return []


    def getCompactible(self, packagetype):
        for plugin in self.package_handlers:
            if packagetype in self.plugins[plugin].packagetype: yield plugin


    def parse_package(self, event_package):
        itemscopy = event_package.items.copy()
        plugins = [asyncio.ensure_future(self.plugins[i].package_handler(self.tools, event_package)
                ) for i in self.getCompactible(event_package.type)]
                
        self.tools.plugin = 'message_handler'
        
        reaction = loop.run_until_complete(
            asyncio.gather(*plugins)
            )

        if len(reaction) == 0:
            reaction.append([self.tools.getValue("NOREACT")])

        for i in reaction:
            if isinstance(i, (list, tuple)):
                if isinstance(i, tuple): i = list(i)
                event_package.items = i

                try:
                    if event_package.items[0] == self.tools.getValue("LIBRARY"):
                        if event_package.items[1] == self.tools.getValue("LIBRARY_NOSELECT"):
                            event_package.items[1] = [
                                (e, self.plugins[e].name) for e in self.plugins.keys() if e not in ['canarycore', 'static', *self.hidelist]
                            ]

                        elif event_package.items[1] in self.plugins.keys():
                            event_package.items.append(self.plugins[event_package.items[1]].version)
                            event_package.items.append(self.plugins[event_package.items[1]].description)
                                

                        else:
                            event_package.items[1] = self.tools.getValue("LIBRARY_ERROR")

                    elif event_package.items[0] == self.tools.getValue("PARSER"):
                        for message in event_package.items[1:-1]:
                            message.from_id = event_package.from_id
                            message.peer_id = event_package.peer_id

                            if hasattr(message, 'fwd_messages'): del message.fwd_messages
                            if hasattr(message, 'reply_message'): del message.reply_message

                            self.parse(message)

                        del event_package.items[1:]

                        event_package.items.append(self.tools.getValue("FWD_MES"))
                        event_package.items.append(self.tools.getValue("ENDLINE"))
                    plugins = [loop.create_task(
                            self.plugins[i].error_handler(self.tools, event_package)
                            ) for i in self.error_handlers]

                    loop.run_until_complete(asyncio.wait(plugins))

                except Exception as e:
                    self.tools.system_message(traceback.format_exc())

        if len(event_package.items) != 0:
            response = self.tools.getValue("MESSAGE_HANDLER_TYPE").value + '\n'
            if event_package.peer_id != event_package.from_id:
                response += self.tools.getValue("MESSAGE_HANDLER_CHAT").value + '\n'

            response += self.tools.getValue("MESSAGE_HANDLER_USER").value + '\n'
            response += self.tools.getValue("MESSAGE_HANDLER_ITEMS").value + '\n'
            if hasattr(event_package, 'text'): response += self.tools.getValue("MESSAGE_HANDLER_IT").value + '\n'
            
            response = response.format(
                peer_id = event_package.peer_id,
                from_id = event_package.from_id,
                event_type = event_package.type.value,
                items = itemscopy[:-1],
                text = event_package.text
            )
            self.tools.system_message(response)
        

class longpoll:
    def __init__(self, session, method, group_id):
        self.session = session
        self.method = method
        self.group_id = str(group_id)
        
        self.url = None
        self.key = None
        self.server = None
        self.ts = None

        self.timeout = aiohttp.ClientTimeout(total = 35)

        init_async(self.update_longpoll_server())
        

    async def update_longpoll_server(self, update_ts=True):
        values = {
            'group_id': self.group_id
        }
        response = await self.method('groups.getLongPollServer', values)

        self.key = response['key']
        self.server = response['server']

        self.url = self.server

        if update_ts:
            self.ts = response['ts']


    async def check(self):
        values = {
            'act': 'a_check',
            'key': self.key,
            'ts': self.ts,
            'wait': 25,
        }

        response = await self.session.get(
            self.url,
            params = values,
            timeout = self.timeout
        )
        response = await response.json()

        if 'failed' not in response:
            self.ts = response['ts']
            return response['updates']

        elif response['failed'] == 1:
            self.ts = response['ts']

        elif response['failed'] == 2:
            await self.update_longpoll_server(update_ts=False)

        elif response['failed'] == 3:
            await self.update_longpoll_server()

        return []


class tools:
    def __init__(self, number, api, http):
        self.__db = Databases(("system", "system.db"))
        self.get = self.__db.get

        self.plugin = "system"
        self.__log = assets("log.txt", "a+", encoding="utf-8")

        self.group_id = number
        self.api = api
        self.http = http
        loop.run_until_complete(self.__setShort())

        self.group_mention = f'[club{self.group_id}|@{self.group_address}]'
        self.mentions = [self.group_mention]
        self.mentions_name_cases = []


        for print_test in self.getValue("LOGGER_START").value:
            print(print_test, 
                file = self.__log
                )
                
        self.__log.flush()

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
        
        try:
            print(f"{self.getDateTime()} {response}", file=self.__log)
        
        except ValueError:
            self.__log = assets("log.txt", "a+", encoding="utf-8")



        self.__log.flush()


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

def init_async(coroutine: asyncio.coroutine):
    return loop.run_until_complete(coroutine)

assets = _assets()
supporting = [objects.static, 0.801, 0.802]