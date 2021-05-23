import threading
import time
from console_util import Console


class IoUtil(threading.Thread):

    def __init__(self, msg, end, level):
        super().__init__()
        self.exit_flag = False
        self.msg = msg
        self.end = end
        self.level = level

    def run(self):
        if self.msg is None or self.end is None or self.level is None:
            return

        i = 0
        n = len(self.msg)

        while True:
            if self.exit_flag:
                return
            else:
                caps_pos = i % n
                decorated_msg = (
                        self.msg[:caps_pos] + self.msg[caps_pos:caps_pos + 2].upper() + self.msg[caps_pos + 2:])
                Console.print_verbose(lmsg=decorated_msg, rmsg='[' + Console.circular_cursor[i % 4] + ']', end=self.end,
                                      level=self.level)
            i += 1
            time.sleep(0.1)
