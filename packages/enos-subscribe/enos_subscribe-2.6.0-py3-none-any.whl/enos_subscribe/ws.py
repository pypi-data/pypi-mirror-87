import websocket
import hashlib
from websocket import WebSocket

from .error import EnosClientInnerParamsError

from .proto import sub_pb2


def sign(access_key=None, sub_id=None, secret=None):
    m = hashlib.sha256()
    m.update(b'access_key')
    m.update(access_key.encode('utf8'))
    m.update(b'access_secret')
    m.update(secret.encode('utf8'))
    m.update(b'sub_id')
    m.update(sub_id.encode('utf8'))
    return m.hexdigest()


class EnosClientWebSocket(WebSocket):

    def on_message(self, message):
        """
        receive message from subscription server
        maybe sub response or pull result
        :return:
        """
        print(message)
        None

    def on_error(self, error):
        """
        retry connect
        :return:
        """
        None

    def on_close(self):
        """
        manually close this client
        :return:
        """
        None

    def on_open(self):
        """
        launch auth task
        :return:
        """
        print('on open')
        auth_req = sub_pb2.AuthReq()
        auth_req.accessKey = self.access_key
        auth_req.subId = self.sub_id
        auth_req.sign = sign(self.access_key, self.subId, self.secret)
        auth_req.subType = self.sub_type

        self.send_binary(auth_req.SerializeToString())

    def __init__(self, address=None, access_key=None, secret=None, sub_id=None, sub_type=None, **_):
        super().__init__(**_)
        if not address:
            raise EnosClientInnerParamsError("subscribe server address is empty")
        if not access_key:
            raise EnosClientInnerParamsError("access key is empty")
        if not secret:
            raise EnosClientInnerParamsError("access secret is empty")
        if not sub_id:
            raise EnosClientInnerParamsError("sub id is empty")
        if not sub_type:
            raise EnosClientInnerParamsError("sub type is empty")

        self.address = address
        self.access_key = access_key
        self.secret = secret
        self.sub_id = sub_id
        self.sub_type = sub_type

        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(address,
                                         on_error=self.on_error,
                                         on_message=self.on_message,
                                         on_close=self.on_close,
                                         on_open=self.on_open)

    def start(self):
        print('start')
        self.ws.run_forever()


if __name__ == "__main__":
    client = EnosClientWebSocket(address='127.0.0.1:9001',
                                 access_key='ea199c3e-f272-4e3d-96af-c59a707322cc',
                                 secret='ea199c3e-f272-4e3d-96af-c59a707322cc',
                                 sub_id='sub-1573716301144',
                                 sub_type='0')
    client.start()
