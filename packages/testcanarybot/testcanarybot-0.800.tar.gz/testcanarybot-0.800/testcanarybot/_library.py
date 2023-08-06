from ._tools import tools
from ._events import events
from .objects import Object
from .objects import package 
from .objects import message 
from .objects import staticPlugin

import os
import traceback
import importlib
import json
import asyncio


class _ohr:
    from_id = ['deleter_id', 'liker_id', 'user_id']
    peer_id = ['market_owner_id', 'owner_id', 'object_owner_id', 
                'post_owner_id', 'photo_owner_id', 'topic_owner_id', 
                'video_owner_id', 'to_id'
                ]


class library:
    def __init__(self, v, group_id, api, http):
        self.loop = asyncio.get_event_loop()

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

        self.loop.run_until_complete(asyncio.gather(*[
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
            pluginObj = staticPlugin()
            self.plugins[plugin] = pluginObj


    def send(self, event):
        event['type'] = event['type'].upper()
        if event['type'] == "MESSAGE_NEW":
            self.parse(
                message(**event['object']['message'])
            )

        else:
            if event['type'] in events.list:
                self.parse_package(
                    self.object_handler(event['type'], event['object'])
                )


    def object_handler(self, event, obj):
        package_handled = package
        package_handled.peer_id = obj['user_id']

        for key, value in obj.items():
            if key in _ohr.peer_id: 
                package_handled.peer_id = value

            if key in _ohr.from_id: 
                package_handled.from_id = value

            package_handled[key] = value
        
        package_handled.items.append(event)
        package_handled.items.append(self.tools.getObject("ENDLINE"))
        package_handled.type = getattr(events, event)
        package_handled.__dict__.update(
            obj
        )

        return package_handled


    def parse(self, message):
        message.type = events.MESSAGE_NEW
        message.items = []

        if hasattr(message, 'action'):
            message.items = [self.tools.getValue("ACTION")]

        elif hasattr(message, 'payload'):
            message.items = [self.tools.getValue("PAYLOAD")]
            message.payload = json.loads(message.payload)

        elif hasattr(message, 'text') and message.text != '': 
            message.items = self.parse_command(message.text)
            
        message.items.append(self.tools.getValue("ENDLINE"))
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
        
        if self.tools.getValue("ADD_MENTIONS").value and response == []:
            for word in message:
                if word.lower() in [*self.tools.getValue("MENTIONS").value, 
                                    *self.tools.getValue("MENTION_NAME_CASES").value]: 
                    response.append(self.tools.getValue("MENTION"))

        if not self.tools.getValue("ONLY_COMMANDS").value and response == []:
            response.append(self.tools.getValue("NOT_COMMAND"))

        return response


    def getCompactible(self, packagetype):
        for plugin in self.package_handlers:
            if packagetype in self.plugins[plugin].packagetype: yield plugin


    def parse_package(self, package):
        plugins = [asyncio.ensure_future(self.plugins[i].package_handler(self.tools, package)
                ) for i in self.getCompactible(package.type)]
                
        self.tools.plugin = 'message_handler'
        
        results = self.loop.run_until_complete(
            asyncio.gather(*plugins)
            )
        self.error_handler(package, results)


    def error_handler(self, package, reaction):
        if len(reaction) == 0:
            reaction.append([self.tools.getValue("NOREACT")])

        for i in reaction:
            if isinstance(i, (list, tuple)):
                if isinstance(i, tuple): i = list(i)
                package.items = i

                try:
                    if package.items[0] == self.tools.getValue("LIBRARY"):
                        if package.items[1] == self.tools.getValue("LIBRARY_NOSELECT"):
                            package.items[1] = [
                                (e, self.plugins[e].name) for e in self.plugins.keys() if e not in ['canarycore', 'static', *self.hidelist]
                            ]

                        elif package.items[1] in self.plugins.keys():
                            package.items.append(self.plugins[package.items[1]].version)
                            package.items.append(self.plugins[package.items[1]].description)
                                

                        else:
                            package.items[1] = self.tools.getValue("LIBRARY_ERROR")

                    elif package.items[0] == self.tools.getValue("PARSER"):
                        for message in package.items[1:-1]:
                            message.from_id = package.from_id
                            message.peer_id = package.peer_id

                            if hasattr(message, 'fwd_messages'): message.fwd_messages = None
                            if hasattr(message, 'reply_message'): message.reply_message = None

                            self.parse(message)

                        del package.items[1:]

                        package.items.append(self.tools.getValue("FWD_MES"))
                        package.items.append(self.tools.getValue("ENDLINE"))
                    plugins = [self.loop.create_task(
                            self.plugins[i].error_handler(self.tools, package)
                            ) for i in self.error_handlers]

                    self.loop.run_until_complete(asyncio.wait(plugins))

                except Exception as e:
                    self.tools.system_message(traceback.format_exc())

        response = self.tools.getValue("MESSAGE_HANDLER_TYPE").value + '\n'
        if package.peer_id != package.from_id:
            response += self.tools.getValue("MESSAGE_HANDLER_CHAT").value + '\n'

        response += self.tools.getValue("MESSAGE_HANDLER_USER").value + '\n'
        response += self.tools.getValue("MESSAGE_HANDLER_ITEMS").value + '\n'
        response = response.format(
            peer_id = package.peer_id,
            from_id = package.from_id,
            event_type = package.type.value,
            items = package.items[:-1]
        )
        self.tools.system_message(response)
        

        

