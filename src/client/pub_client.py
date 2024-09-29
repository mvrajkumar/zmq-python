import zmq
import sys
import threading
import logging

from datetime import datetime

logging.basicConfig(filename='subscriber.log', level=logging.INFO)

HOST = 'localhost'
PORT = '5570'

def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


class CompClientTask(threading.Thread):
    """ClientTask

    These are the Followers
    """

    def __init__(self, id, host=HOST, port=PORT):
        self.id = id
        threading.Thread.__init__(self)
        self.timing_channel_workers = {}
        self.timing_channel_workers["0"] = []
        self.timing_channel_workers["1"] = []
        self.host = host
        self.port = port
        for i in range(4):
            channel = str(i % 2)
            worker = demoLocalWorker(
                self.id * 100 + i, channel
            )  
            self.timing_channel_workers[channel].append(worker)

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        identity = "sub-%d" % self.id
        socket.connect('tcp://{}:{}'.format(self.host, self.port))
        print("Subscriber %s started successfully" % (identity))

        for channel in self.timing_channel_workers.keys():
            socket.setsockopt_string(zmq.SUBSCRIBE, channel)

        #print("Client %s has now subscribed to channel %s and accepting messages" % (identity,channel))

        while True:
            msg = socket.recv_string()
            channel, time_str = msg.split()

            tprint("Hello World!! Subscriber %s received message on Channel: %s" % (identity, msg))
            logging.info(
                '{}   - {}'.format(msg, time_str))
            if channel in self.timing_channel_workers.keys():
                timestamp = datetime.fromisoformat(time_str)
                #for worker in self.timing_channel_workers[channel]:
                #    worker.call(timestamp)

            # Using recv_multipart
            msg = socket.recv_multipart()
            #tprint("Client %s received: %s" % (identity, msg))
            channel = msg[0].decode()
            if channel in self.timing_channel_workers.keys():
                timestamp = datetime.fromisoformat(msg[1].decode())
                #for worker in self.timing_channel_workers[channel]:
                #    worker.call(timestamp)

        socket.close()
        context.term()

class demoLocalWorker:

    def __init__(self, id: int, channel: str = "default") -> None:
        self.id = id
        self.channel = channel

    def call(self, timestamp: datetime):
        print(
            "Timestamp = %s ID = %s Channel = %s"
            % (timestamp, self.id, self.channel)
        )


def main():
    """main function"""
    for i in range(3):
        client = CompClientTask(i)
        client.start()

if __name__ == "__main__":
    main()
