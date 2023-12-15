"""
Contains SNMPmonitor class
"""
from os import get_terminal_size, system
from time import sleep
from threading import Thread
from art import tprint
from nmap import PortScanner
from netifaces import interfaces, ifaddresses, AF_INET
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity import config
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.hlapi import *
from data import Host, Iface

TERM_WIDTH = get_terminal_size().columns


class SNMPmonitor:
    """
    Network-monitoring system
    """

    def __init__(self):
        tprint("SNMP Monitor")
        self.devices = []
        self.host = Host()
        for interface in interfaces():
            for link in ifaddresses(interface)[AF_INET]:
                if '127' not in link['addr'] and '172' not in link['addr']:
                    mask = str(sum([(sum(list(map(int, i))))
                                    for i in [format(int(i), 'b')
                                              for i in link['netmask'].split('.') if
                                              i != '0']]))
                    self.host.interfaces.append(
                        Iface(f"{link['addr']}/{mask}"))
        self.find_devs()

    def find_devs(self):
        """
        Detect active devices in network
        :return:
        """
        system('clear')
        tprint("SNMP Monitor (Beta)")
        print("Scanning network...")
        scanner = PortScanner()
        for eth in self.host.interfaces:
            addr, mask = eth.address.split('/')
            ip_range = f"{addr[:addr.rfind('.')]}.0/{mask}"
            scanner.scan(hosts=ip_range, arguments='-sn')
            for iface in scanner.all_hosts():
                eths = [Iface(iface, scanner[addr]['status']['state'])]
                self.devices.append(Host(interfaces=eths, status="Active"))

        for dev in self.devices:
            for eth in dev.interfaces:
                print(f" - New device({eth})")
                data = self.snmp_get(eth.address, '1.3.6.1.2.1.1.1.0')
                if data:
                    dev.hostname = data[3]
                    dev.system = data[5]
                else:
                    dev.status = 'Unreachable'

        for dev in self.devices:
            for _dev in self.devices:
                if dev != _dev:
                    if dev.hostname == _dev.hostname:
                        dev.interfaces += _dev.interfaces
                        self.devices.remove(_dev)
        sleep(10)
        system('clear')
        tprint("SNMP Monitor (Beta)")
        print(f"\n{'=' * TERM_WIDTH}")
        for dev in self.devices:
            if dev.hostname == 'manager':
                print(f"|| LOCAL: {dev} \n{'=' * TERM_WIDTH}")
            else:
                print(f"|| REMOTE: {dev} \n{'=' * TERM_WIDTH}")

    @staticmethod
    def snmp_get(ip_addr: str, oid: str) -> list:
        """
        Realise snmp-get function
        :param ip_addr: ip address of target device
        :param oid: snmp object identifier
        :return:
        """
        print('\tGetting information...')
        error_indication, error_status, error_index, var_binds = next(
            getCmd(SnmpEngine(),
                   CommunityData('test'),
                   UdpTransportTarget((ip_addr, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity(oid)))
        )
        if len(var_binds) > 0:
            print('\tDone')
            return var_binds[0].prettyPrint().split(' ')
        else:
            print('\tNo information')
            return []

    @staticmethod
    def snmp_walk(ip_addr: str, oid: str) -> list:
        """
        Realise snmp-walk function
        :param ip_addr: ip address of target device
        :param oid: snmp object identifier
        :return:
        """
        error_indication, error_status, error_index, var_binds = next(
            nextCmd(SnmpEngine(),
                    CommunityData('test'),
                    UdpTransportTarget((ip_addr, 161)),
                    ContextData(),
                    ObjectType(ObjectIdentity(oid)))
        )
        if len(var_binds) > 0:
            return var_binds[0].prettyPrint().split(' ')[-1]
        else:
            return []

    @staticmethod
    def operate_trap(snmp_engine, state_reference, context_engine_id, context_ame,
                     var_binds, cb_ctx):
        """
        Notify manager about incoming snmp-traps
        Calls from `NotificationReceiver()`
        Params passing by default
        :param snmp_engine:
        :param state_reference:
        :param context_engine_id:
        :param context_ame:
        :param var_binds:
        :param cb_ctx:
        :return:
        """
        print("Received new Trap message")
        for name, val in var_binds:
            print(f"{name.prettyPrint()} = {val.prettyPrint()}")

    @staticmethod
    def listen_trap():
        """
        Start snmp-trap listener
        :return:
        """
        snmp_engine = SnmpEngine()
        config.addTransport(
            snmp_engine,
            udp.domainName,
            udp.UdpTransport().openServerMode(('0.0.0.0', 1162))
        )

        config.addV1System(snmp_engine, 'test-area', 'test')
        ntfrcv.NotificationReceiver(snmp_engine, SNMPmonitor.operate_trap)
        snmp_engine.transportDispatcher.jobStarted(1)
        print(
            f"Listening for incoming SNMP TRAP messages...\n\n{'=' * TERM_WIDTH}")
        snmp_engine.transportDispatcher.runDispatcher()

    def run(self):
        """
        Start network monitoring
        :return:
        """
        print("\nMonitoring remote hosts...")
        trap_th = Thread(target=self.listen_trap)
        trap_th.start()
        while True:
            for dev in self.devices:
                cpu_info = self.snmp_walk(
                    dev.interfaces[0].address, '1.3.6.1.2.1.25.3.3.1.2')
                network_info = self.snmp_walk(
                    dev.interfaces[0].address, '1.3.6.1.2.1.2.2.1.10')
                if cpu_info and network_info:
                    print(f"{dev.hostname}({dev.interfaces[0].address}):")
                    print(f"\tTotal bytes received: {network_info}")
                    print(f"\tCPU usage: {cpu_info}%")
                    print('=' * TERM_WIDTH)
            sleep(10)


if __name__ == '__main__':
    monitor = SNMPmonitor()
    monitor.run()
