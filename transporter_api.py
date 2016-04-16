import zmq
from zmq.eventloop import ioloop, zmqstream
import functools
import time


class Transporter:
    def on_receive(self, msg):
        print "Received:", msg

    def bind_receive(self, ip, port):
        incoming = zmq.Context().socket(zmq.PULL)
        incoming.bind('tcp://' + ip + ':' + str(port))
        sincoming = zmqstream.ZMQStream(incoming)
        sincoming.on_recv(functools.partial(self.on_receive))

    def send_message(self, ip, port, msg):
        ctk = zmq.Context()
        outgoing = ctk.socket(zmq.PUSH)
        # outgoing.hwm = 1
        outgoing.connect('tcp://' + ip + ':' + str(port))
        outgoing.send_json(msg, zmq.NOBLOCK)
        soutgoing = zmqstream.ZMQStream(outgoing)
        soutgoing.on_send(functools.partial(self.on_receive))
        ctk.destroy(linger=100)

    def send_message_node(self, node, msg):
        outgoing = zmq.Context().socket(zmq.PUSH)
        outgoing.connect('tcp://' + node.ip + ':' + str(node.port))
        outgoing.send_json(msg)

    def start_listening(self):
        ioloop.IOLoop.instance().start()
