"""
values for `python -m testcanarybot -c`
"""


module_cover = """{package_handler_import}class Main:
    async def start(self, tools):
        self.name = "{name}"
        self.version = 0.8
        self.description = \"\"\"
            {descr}\"\"\"{package_events}
        
        {package_handler}{error_handler}
"""
package_events = """
        self.packagetype = [
            # events.MESSAGE_NEW
        ]"""
package_handler = """
    async def package_handler(self, tools, package):
        # tools: testcanarybot.tools
        # package: formatted into message object got from longpoll server
        pass

"""
package_handler_import = """from testcanarybot import events # for Main.package_handler
"""
error_handler = """
    async def error_handler(self, tools, package):
        # tools: testcanarybot.tools
        # package: formatted into message object got from longpoll server
        pass
"""