from flask import Flask, request
from waitress import serve
import uuid, asyncio, json
from functools import wraps

from notifybot.task import TaskId

route_map = {}

def route(url, methods=['GET']):
    def inner_decorator(f):
        if url not in route_map:
            route_map[url] = {}
        for method in methods:
            route_map[url][method] = f 
        return f
    return inner_decorator

class WebServer:

    def __init__(self, task):
        self.task = task
        self.app = Flask(__name__)
        self.app.config['JSON_AS_ASCII'] = False

        for r in route_map:
            for m in route_map[r]:
                f = getattr(self, route_map[r][m].__name__)
                f = self.app.route(r, methods=[m])(f)

    def run(self, port):
        if __debug__:
            return self.app.run(host="0.0.0.0", port=port, use_reloader=False, debug=False)
        else:
            return serve(self.app, host='0.0.0.0', port=port)

    def result(self, success, data):
        return {"success": success, "data": data}

    # authorization
    def set_auth(self, user, password):
        self.user = user
        self.password = password

    def check_auth(self, authorization):
        result = True
        if hasattr(self, 'user') and hasattr(self, 'password'):
            if not isinstance(authorization, dict) or \
                authorization.get("username") != self.user or \
                authorization.get("password") != self.password:
                result = False

        return result

    def require_auth(f):
        @wraps(f)
        async def decorated(self, *args, **kwargs):
            if not self.check_auth(request.authorization):
                return self.result(False, "Authorization failed")
            return await f(self, *args, **kwargs)
        return decorated

    # requests
    @route('/send_text', methods=['POST'])
    @require_auth
    async def send_text(self):
        content = request.json
        success, data = await self.task.async_request(TaskId.SEND_TEXT, request.json)
        return self.result(success, data)

    @route('/send_embed', methods=['POST'])
    @require_auth
    async def send_embed(self):
        content = request.json      
        success, data = await self.task.async_request(TaskId.SEND_EMBED, request.json)
        return self.result(success, data)

    @route('/get_channels', methods=['GET'])
    @require_auth
    async def get_channels(self):
        success, data = await self.task.async_request(TaskId.GET_CHANNEL, None)
        return self.result(success, data)

    @route('/get_members', methods=['GET'])
    @require_auth
    async def get_members(self):
        success, data = await self.task.async_request(TaskId.GET_MEMBER, None)
        return self.result(success, data)

    