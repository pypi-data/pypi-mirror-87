from __future__ import absolute_import

import copy
import logging
import time

from .error import EnosClientConfigurationError
from .core import SocketClient
from .structs import TopicPartition
from .proto import sub_pb2
from .vendor import six

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

DEFAULT_CONFIG = {
    'host': None,
    'port': 9001,
    'access_key': None,
    'access_secret': None,
    'sub_id': None,
    'consumer_group': '',
    'auto_commit_interval_seconds': 5,
    'sub_type': 0
}

NOT_MATCHED_MESSAGE = '_*NMM!_'


def do_commit(consumer_offsets, ws):
    if len(consumer_offsets.keys()) > 0:
        commit_dto = sub_pb2.CommitDTO()
        for key in consumer_offsets.keys():
            tp = key
            offset = consumer_offsets[tp]
            commit = commit_dto.commits.add()
            commit.topic = tp.topic
            commit.partition = tp.partition
            commit.offset = offset
        try:
            ws.commit_offsets(commit_dto)
        except (Exception, KeyboardInterrupt, SystemExit) as e:
            log.debug('Commit offset error', e)


class DataClient(six.Iterator):

    def __init__(self, **configs):
        extra_configs = set(configs).difference(DEFAULT_CONFIG)
        if extra_configs:
            raise EnosClientConfigurationError("Unrecognized configs: %s" % (extra_configs,))

        self.config = copy.copy(DEFAULT_CONFIG)
        self.config.update(configs)
        if not self.config['sub_type']:
            self.config['sub_type'] = 0
        self.ws_client = None
        self._iterator = None
        self.consumer_offset = {}
        self.auto_commit_interval = self.config['auto_commit_interval_seconds']
        self.next_auto_commit_deadline = None

    def __iter__(self):
        return self

    def subscribe(self, sub_id=None, consumer_group='DefaultConsumerGroup'):
        host = self.config['host']
        port = self.config['port']
        access_key = self.config['access_key']
        access_secret = self.config['access_secret']

        self.ws_client = SocketClient(server_address=host,
                                      port=port,
                                      access_key=access_key,
                                      access_secret=access_secret,
                                      sub_id=sub_id,
                                      sub_type=self.config['sub_type'],
                                      consumer_group=consumer_group)
        self.next_auto_commit_deadline = time.time() + self.auto_commit_interval
        self.ws_client.start()

    def __next__(self):
        next_message = self.next_message()
        return next_message

    def next_message(self):
        if not self._iterator:
            self._iterator = self._message_generator()

        if time.time() > self.next_auto_commit_deadline:
            do_commit(self.consumer_offset, self.ws_client)
            self.consumer_offset = {}
            self.next_auto_commit_deadline = self.next_auto_commit_deadline + self.auto_commit_interval

        while True:
            next_message = next(self._iterator)
            topic = next_message.topic
            partition = next_message.partition
            offset = next_message.offset
            value = next_message.value
            self.consumer_offset[TopicPartition(topic, partition)] = offset

            if '_*NMM!_' != value:
                break

        return value

    def _message_generator(self):
        while True:
            yield self.ws_client.poll()


class AlertClient(DataClient):
    def __init__(self, **configs):
        configs['sub_type'] = 1
        super().__init__(**configs)


class OfflineClient(DataClient):
    def __init__(self, **configs):
        configs['sub_type'] = 3
        super().__init__(**configs)


class EventClient(DataClient):
    def __init__(self, **configs):
        configs['sub_type'] = 4
        super().__init__(**configs)


class AdvancedAlertClient(DataClient):
    def __init__(self, **configs):
        configs['sub_type'] = 5
        super().__init__(**configs)


# if __name__ == '__main__':
#     client = DataClient(host='10.27.21.246', port='9001',
#                         access_key='ea199c3e-f272-4e3d-96af-c59a707322cc',
#                         access_secret='9f545c81-9839-4907-999e-307724b40183')
#
#     client.subscribe(sub_id='sub-1573716301144')
#
#     for message in client:
#         print(message)

    # consumer_offsets_ = {
    #     TopicPartition('topic1', 1): 123,
    #     TopicPartition('topic2', 2): 456
    # }
    #
    # print(do_commit(consumer_offsets_))
    # word = '_*NMM!_'
    # print('_*NMM!_' == word)
