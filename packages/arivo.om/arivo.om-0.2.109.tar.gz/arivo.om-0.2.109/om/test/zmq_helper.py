from __future__ import unicode_literals

import threading
import time

import zmq
from om.message import Message


class ZMQTestMixin(object):
    ZMQ_SUB_PORT = 10100
    ZMQ_PUB_PORT = 10200
    _command_topic = b"_testcase_commands"
    ZMQ_STARTUP_SLEEP = 1
    topics = []

    def _start_broker(self):
        def broker():
            alpr_endpoint = self.zmq_context.socket(zmq.XSUB)
            service_endpoint = self.zmq_context.socket(zmq.XPUB)
            alpr_endpoint.setsockopt(zmq.LINGER, 0)
            service_endpoint.setsockopt(zmq.LINGER, 0)
            alpr_endpoint.bind("tcp://*:{}".format(self.ZMQ_SUB_PORT))
            service_endpoint.bind("tcp://*:{}".format(self.ZMQ_PUB_PORT))
            try:
                zmq.proxy(alpr_endpoint, service_endpoint)
            except zmq.ContextTerminated:
                pass
            alpr_endpoint.close()
            service_endpoint.close()

        thread = threading.Thread(target=broker)
        thread.start()
        return thread

    def _zmq_sub_recvloop(self):
        while True:
            topic, message = Message.from_socket(self.zmq_sub)
            if topic == self._command_topic:
                if message["cmd"] == "hi":
                    self.zmq_connected.set()
                elif message["cmd"] == "exit":
                    break
            else:
                with self.zmq_recv_lock:
                    self.zmq_recv_messages.append((topic, message))
                    self.zmq_has_messages.set()

    def _start_zmq(self):
        self.zmq_connected = threading.Event()
        self.zmq_context = zmq.Context()
        self.zmq_broker_thread = self._start_broker()
        self.zmq_pub = self.zmq_context.socket(zmq.PUB)
        self.zmq_pub.setsockopt(zmq.LINGER, 0)
        self.zmq_pub.connect("tcp://127.0.0.1:10100")
        self.zmq_sub = self.zmq_context.socket(zmq.SUB)
        self.zmq_sub.setsockopt(zmq.LINGER, 0)
        self.zmq_sub.connect("tcp://127.0.0.1:10200")
        self.zmq_sub.subscribe(self._command_topic)
        self.zmq_sub_thread = threading.Thread(target=self._zmq_sub_recvloop)
        self.zmq_sub_thread.start()
        self.zmq_recv_lock = threading.Lock()
        self.zmq_recv_messages = []
        self.zmq_has_messages = threading.Event()

        for x in range(20):
            self._zmq_cmd("hi")
            self.zmq_connected.wait(timeout=0.05)
        assert self.zmq_connected.is_set(), "broker startup and connect failed"

        time.sleep(self.ZMQ_STARTUP_SLEEP)
        for topic in self.topics:
            self.zmq_subscribe(topic)

    def _zmq_cmd(self, cmd):
        Message(cmd=cmd).to_socket(self.zmq_pub, self._command_topic)

    def _stop_zmq(self):
        self._zmq_cmd("exit")
        self.zmq_sub_thread.join()
        self.zmq_sub.close()
        self.zmq_pub.close()
        self.zmq_context.term()
        self.zmq_broker_thread.join()

    def zmq_subscribe(self, topic):
        self.zmq_sub.subscribe(topic)

    def zmq_send(self, topic, _message=None, **kwargs):
        data = _message or kwargs
        assert not (_message and kwargs), "pass the message dict as the first parameter, or use the kwargs, not both"
        assert "type" in data, "a message must always have a type"
        if "name" not in data:
            data["name"] = "testcase"
        Message(**data).to_socket(self.zmq_pub, topic)

    def _zmq_pop_from_front(self):
        with self.zmq_recv_lock:
            msg = self.zmq_recv_messages.pop(0)
            if not self.zmq_recv_messages:
                self.zmq_has_messages.clear()
            return msg

    def zmq_wait_for_message(self, topic=None, timeout=1):
        start = time.time()
        while True:
            if not self.zmq_has_messages.wait(timeout=timeout):
                raise TimeoutError()

            while self.zmq_recv_messages:
                message_topic, message = self._zmq_pop_from_front()
                if not topic or message_topic == topic:
                    return topic, message

            time_diff = time.time() - start
            if time_diff > timeout:
                raise TimeoutError()

    def setUp(self):
        super(ZMQTestMixin, self).setUp()
        self._start_zmq()

    def tearDown(self):
        super(ZMQTestMixin, self).tearDown()
        self._stop_zmq()
