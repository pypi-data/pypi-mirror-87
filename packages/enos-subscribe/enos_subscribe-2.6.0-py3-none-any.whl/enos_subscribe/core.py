import copy
import hashlib
import logging
import queue
import socket
import threading
import time

try:
    import thread
except ImportError:
    import _thread as thread

import websocket

from .error import EnosClientConfigurationError

from websocket import create_connection

from .proto import sub_pb2
from .proto import common_pb2

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

_CMD_MAP = {
    0: sub_pb2.IdleReq,
    1: sub_pb2.IdleRsp,
    2: sub_pb2.AuthReq,
    3: sub_pb2.AuthRsp,
    4: sub_pb2.PullReq,
    5: sub_pb2.PullRsp,
    6: sub_pb2.SubReq,
    7: sub_pb2.SubRsp
}

_MESSAGE_MAP = {
    sub_pb2.IdleReq: 0,
    sub_pb2.IdleRsp: 1,
    sub_pb2.AuthReq: 2,
    sub_pb2.AuthRsp: 3,
    sub_pb2.PullReq: 4,
    sub_pb2.PullRsp: 5,
    sub_pb2.SubReq: 6,
    sub_pb2.SubRsp: 7,
    sub_pb2.CommitDTO: 8
}

DEFAULT_MESSAGE_QUEUE_SIZE = 100


def sign(access_key=None, sub_id=None, secret=None):
    # Sign the access request, SHA256
    m = hashlib.sha256()
    m.update(b'access_key')
    m.update(access_key.encode('utf8'))
    m.update(b'access_secret')
    m.update(secret.encode('utf8'))
    m.update(b'sub_id')
    m.update(sub_id.encode('utf8'))
    return m.hexdigest()


def pkg_parser(message):
    pkg = common_pb2.TransferPkg().FromString(message)
    cmd_id = pkg.cmdId
    data = pkg.data

    return _CMD_MAP[cmd_id], _CMD_MAP[cmd_id].FromString(data)


def build_pkg(cmd_id, data):
    transfer_pkg = common_pb2.TransferPkg()
    transfer_pkg.seqId = 0
    transfer_pkg.cmdId = cmd_id
    transfer_pkg.data = data
    transfer_pkg.zip = False
    transfer_pkg.ver = 0

    return transfer_pkg.SerializeToString()


def run(*args):
    ws_client = args[0]
    epoch = ws_client.epoch
    while ws_client.connected:
        if epoch != ws_client.epoch:
            return
        ws_client.pull_once()
    log.info("socket already closed")


def lifecycle_keeper(*args):
    ws_client = args[0]
    epoch = ws_client.epoch
    while ws_client.connected:
        if epoch != ws_client.epoch:
            return
        if time.time() > ws_client.next_ping_deadline:
            ws_client.ping_and_recv()
            ws_client.next_ping_deadline = ws_client.next_ping_deadline + ws_client.ping_interval
        else:
            time.sleep(1)
    log.info("socket already closed")


class SocketClient:
    DEFAULT_CONFIG = {
        'server_address': None,
        'port': '9001',
        'access_key': None,
        'access_secret': None,
        'sub_id': None,
        'sub_type': None,
        'consumer_group': ''
    }

    def __init__(self, **configs):
        log.debug("config the subscription client")
        extra_configs = set(configs).difference(self.DEFAULT_CONFIG)
        if extra_configs:
            raise EnosClientConfigurationError("Unrecognized configs: %s" % (extra_configs,))

        self.config = copy.copy(self.DEFAULT_CONFIG)
        self.config.update(configs)
        self.ws = None
        self.message_queue = queue.Queue(DEFAULT_MESSAGE_QUEUE_SIZE)
        self.pull_id = 0
        self.lock = threading.RLock()
        self.ping_interval = 10
        self.next_ping_deadline = None
        self.connected = False
        self.epoch = 0

    def start(self):
        log.info("start the subscription client")
        server_address = self.config['server_address']
        port = self.config['port']
        url = """ws://{_address}:{_port}""".format(_address=server_address, _port=port)

        while not self.connected:
            try:
                self.ws = create_connection(url)
                self.connected = True
                time.sleep(1)
            except (Exception, KeyboardInterrupt, SystemExit) as e:
                log.debug('connect fail', e)
        self.epoch = self.epoch + 1
        self.auth()

    """
    restart connect process when exception occur
    """

    def reconnect(self):
        self.message_queue.queue.clear()
        self.start()

    def auth(self):
        auth_req = sub_pb2.AuthReq()
        auth_req.accessKey = self.config['access_key']
        auth_req.subId = self.config['sub_id']
        auth_req.sign = sign(self.config['access_key'],
                             self.config['sub_id'],
                             self.config['access_secret'])
        auth_req.subType = self.config['sub_type']

        auth_bytes = build_pkg(_MESSAGE_MAP[sub_pb2.AuthReq], auth_req.SerializeToString())

        log.info("Send auth: %s", auth_req)

        message = self.send_and_recv(auth_bytes)

        message_type, message_real = pkg_parser(message)

        log.debug("receive message, expect auth response: %s", message_real)

        if message_type == sub_pb2.AuthRsp:
            ack = message_real.ack
            if 0 != ack:
                log.info("Auth fail, auth info: %s", auth_req)
                self.ws.close()
            else:
                self.next_ping_deadline = time.time() + self.ping_interval
                thread.start_new_thread(lifecycle_keeper, (self,))
                self.sub()
        else:
            log.debug("Receive unexpect response, need SubRsp, receive: %s", message_type)
            self.ws.close()

    def sub(self):
        sub_req = sub_pb2.SubReq()
        sub_req.category = self.config['sub_type']
        sub_req.clientId = socket.gethostname()
        sub_req.subId = self.config['sub_id']
        sub_req.accessKey = self.config['access_key']
        sub_req.consumerGroup = self.config['consumer_group']

        sub_bytes = build_pkg(_MESSAGE_MAP[sub_pb2.SubReq], sub_req.SerializeToString())

        log.info("Send sub request: %s", sub_req)

        message = self.send_and_recv(sub_bytes)

        message_type, message_real = pkg_parser(message)

        if message_type == sub_pb2.SubRsp:
            ack = message_real.ack
            if 0 != ack:
                log.info("Sub fail, sub info: %s", sub_req)
                self.ws.close()
            else:
                log.info("Sub success")
                thread.start_new_thread(run, (self,))
        else:
            log.debug("Receive unexpect response, need SubRsp, receive: %s", message_type)
            self.ws.close()

    def pull_once(self):
        pull_req = sub_pb2.PullReq()
        self.pull_id = self.pull_id + 1
        pull_req.id = self.pull_id

        pull_bytes = build_pkg(_MESSAGE_MAP[sub_pb2.PullReq], pull_req.SerializeToString())

        message = self.send_and_recv(pull_bytes)

        message_type, message_real = pkg_parser(message)

        if sub_pb2.PullRsp == message_type:
            msgs = message_real.msgDTO.messages
            for msg in msgs:
                self.message_queue.put(msg)

    def stop(self):
        self.connected = False

    def poll(self):
        return self.message_queue.get()

    def commit_offsets(self, consumer_offsets):
        if consumer_offsets:
            commit_bytes = build_pkg(_MESSAGE_MAP[sub_pb2.CommitDTO], consumer_offsets.SerializeToString())
            log.debug('Commit Offsets: %s', consumer_offsets)
            self.send_and_recv(commit_bytes, need_recv=False)

    def send_and_recv(self, message_to_send=None, need_recv=True):
        self.lock.acquire()
        try:
            if need_recv:
                self.ws.send(message_to_send, websocket.ABNF.OPCODE_BINARY)
                message_recv = self.ws.recv()
                return message_recv
            else:
                self.ws.send(message_to_send, websocket.ABNF.OPCODE_BINARY)
        except (Exception, KeyboardInterrupt, SystemExit) as e:
            log.error('Error occur', e)
            self.connected = False
            self.reconnect()
            raise e
        finally:
            self.lock.release()

    def ping_and_recv(self):
        self.lock.acquire()
        try:
            self.ws.ping()
        except (Exception, KeyboardInterrupt, SystemExit) as e:
            log.error('Error occur', e)
            self.connected = False
            self.reconnect()
            raise e
        finally:
            self.lock.release()


if __name__ == '__main__':
    websocket.enableTrace(True)
    client = SocketClient(server_address='10.27.21.246',
                          access_key='ea199c3e-f272-4e3d-96af-c59a707322cc',
                          access_secret='9f545c81-9839-4907-999e-307724b40183',
                          sub_id='sub-1573716301144',
                          sub_type=0)
    client.start()
