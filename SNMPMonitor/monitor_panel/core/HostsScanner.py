from random import randint
from time import sleep
# from monitor_panel.core.SNMPManager import SNMPManager
from monitor_panel.core.hosts import HOSTS


class HostsScanner:
    def __init__(self):
        # self.manager = SNMPManager()
        # self.manager.find_devs()
        self.counter = 0
        # self.hosts = self.manager.HOSTS
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

    @staticmethod
    def update_state(self, dev: str, key: str, val: any):
        for host in monitor_panel.core.hosts.HOSTS:
            if host.ip == dev:
                setattr(host, key, val)


