from enum import Enum, auto
import threading, uuid, asyncio, time

TIMEOUT = 30

class TaskId(Enum):
    SEND_TEXT = auto()
    SEND_EMBED = auto()
    GET_CHANNEL = auto()
    GET_MEMBER = auto()

class TaskQueue():
    def __init__(self):
        self.request = {}
        self.request_lock = threading.Lock()
        self.response = {}       
        self.response_lock = threading.Lock()

    def add_request(self, id, data = None):
        uid = str(uuid.uuid4())
        self.request_lock.acquire()
        self.request[uid] = Request(id, data)
        self.request_lock.release()
        return uid

    def get_request(self):
        self.request_lock.acquire()
        uid = next(iter(self.request), None)
        id, data = None, None
        if uid is not None:
            request = self.request[uid]
            del self.request[uid]
            id, data = request.id, request.data
        self.request_lock.release()
        return uid, id, data

    def add_response(self, uid, success, data = None):
        self.response_lock.acquire()
        self.response[uid] = Response(success, data)
        self.response_lock.release()

    def get_response(self, uid):
        success, data = None, None
        self.response_lock.acquire()
        if uid in self.response:
            response = self.response[uid]
            del self.response[uid]
            success, data = response.success, response.data
        self.response_lock.release()
        return success, data

    async def async_request(self, id, data = None):
        timeout = time.time() + TIMEOUT
        uid = self.add_request(id, data)
        success = None
        while success == None:
            if time.time() >= timeout:
                success, data = False, "request timeout"
                break
            await asyncio.sleep(0.1)
            success, data = self.get_response(uid)
        return success, data

class Request():
    def __init__(self, id, data):
        self._id = id
        self._data = data

    @property
    def id(self):
        return self._id

    @property
    def data(self):
        return self._data

class Response():
    def __init__(self, success, data):
        self._success = success
        self._data = data

    @property
    def success(self):
        return self._success

    @property
    def data(self):
        return self._data

