import zmq
import threading
import time
import random
from datetime import datetime, timezone

port = "5570"

class ServerAllInOne:
    """ServerAllInOne"""

    def __init__(self):
        self.timingChannels = ["0", "1"]
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % port)
        time.sleep(1)
        self.timing_thread = threading.Thread(target=self.timing_loop)
        self.timing_thread.start()

    def timing_loop(self):
        """Timing loop

        Equivalent of the main timing loop.
        Since we have no specific periods to call workers in this demo just call them at random
        """
        while True:

            timing_channel = random.choice(self.timingChannels)
            print("Publisher is now sending Hello World message using channel %s" % (timing_channel))
            calltime = datetime.now(timezone.utc)

            # Using send_string
            self.socket.send_string(f"{timing_channel} {calltime.isoformat()}")

            # Using send_multipart
            msg = [timing_channel.encode(), calltime.isoformat().encode()]
            self.socket.send_multipart(msg)

            time.sleep(5)

def main():
    """main function"""
    server = ServerAllInOne()
    server.timing_thread.join()


if __name__ == "__main__":
    main()