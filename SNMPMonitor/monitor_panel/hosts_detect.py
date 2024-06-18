from random import randint
from time import sleep
from monitor_panel.hosts import HOSTS


class HostsGenerator:
    def __init__(self):
        self.counter = 0
        self.hosts = HOSTS

    def __iter__(self):
        if self.counter >= len(self.hosts):
            #sleep(5)
            return False
        else:
            res = self.hosts[self.counter]
            self.counter += 1
            #sleep(randint(1, 4))
            yield res

