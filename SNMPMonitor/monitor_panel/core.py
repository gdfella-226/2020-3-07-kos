"""
Contains SNMPmonitor class
"""
from os import get_terminal_size, system, path
from time import sleep
from threading import Thread
from art import tprint
from nmap import PortScanner
from netifaces import interfaces, ifaddresses, AF_INET
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity import config
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.hlapi import *
from monitor_panel.models import Host
from monitor_panel.hosts import HOSTS
from json import load
from uuid import getnode


class MonitorCore:
    """
    Network-monitoring system
    """

    def __init__(self):
        with open(path.join('./', 'SNMPMonitor', 'data.json')) as json_file:
            data = json.load(json_file)
            if data['filter_subnet']:
                self.SUBNET = data['subnet']
        self.devices = []
        self.host = None
        self.params = []
        for interface in interfaces():
            for link in ifaddresses(interface)[AF_INET]:
                if f'.{self.SUBNET}.' in link['addr']:
                    self.params['ip'] = link['addr']
                if link['mac'] == ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                                            for ele in range(0, 8 * 6, 8)][::-1]):
                    self.params['role'] = 'Manager'
                else:
                    self.params['role'] = 'Agent'
        self.find_devs()

    def find_devs(self):
        """
        Detect active devices in network
        :return:
        """
        scanner = PortScanner()
        devs = []
        i = 0
        for eth in self.host.interfaces:
            params.append(dict())
            addr, mask = eth.address.split('/')
            ip_range = f"{addr[:addr.rfind('.')]}.0/{mask}"
            scanner.scan(hosts=ip_range, arguments='-sn')
            for iface in scanner.all_hosts():
                params[i]['status'] = scanner[addr]['status']['state']
                devs.append(iface)
                i += 1

        for dev in self.params:
            data = self.snmp_get(dev['ip'], '1.3.6.1.2.1.1.1.0')
            if data:
                dev['status'] = data[3]
                dev['system'] = data[5]
            else:
                dev['status'] = 'Inactive'
            self.devices.append(Host(ip=self.params['ip'], hostname=self.params['hostname'], role=self.params['role'],
                                     system=self.params['system'], status=self.params['status']))
            for i in self.devices:
                HOSTS.append(i)

    @staticmethod
    def snmp_get(ip_addr: str, oid: str) -> list:
        """
        Realise snmp-get function
        :param ip_addr: ip address of target device
        :param oid: snmp object identifier
        :return:
        """
        error_indication, error_status, error_index, var_binds = next(
            getCmd(SnmpEngine(),
                   CommunityData('test'),
                   UdpTransportTarget((ip_addr, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity(oid)))
        )
        if len(var_binds) > 0:
            return var_binds[0].prettyPrint().split(' ')
        else:
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
        if SNMPmonitor.listen_trap(snmp_engine):
            for name, val in var_binds:
                return name.prettyPrint(), val.prettyPrint()

    @staticmethod
    def listen_trap(snmp_engine):
        """
        Start snmp-trap listener
        :return:
        """
        config.addTransport(
            snmp_engine,
            udp.domainName,
            udp.UdpTransport().openServerMode(('0.0.0.0', 1162))
        )

        config.addV1System(snmp_engine, 'test-area', 'test')
        ntfrcv.NotificationReceiver(snmp_engine, SNMPmonitor.operate_trap)
        snmp_engine.transportDispatcher.jobStarted(1)
        return snmp_engine.transportDispatcher.runDispatcher()

    def update_devs(self):
        """
        Start network monitoring
        :return:
        """
        current_time = datetime.datetime.now()
        for dev in self.params:
            dev['cpu_info'] = self.snmp_walk(
                dev['ip'], '1.3.6.1.2.1.25.3.3.1.2')
            dev['hdd_info'] = self.snmp_walk(
                dev['ip'], '1.3.6.1.2.1.16.2.4.1')
            dev['hdd_total'] = self.snmp_walk(
                dev['ip'], '1.3.6.1.2.1.16.2.4.0')
            dev['network_info'] = self.snmp_walk(
                dev['ip'], '1.3.6.1.2.1.2.2.1.10')
            dev['status'] = self.snmp_get(
                dev['ip'], '1.3.6.1.2.1.1.1.0')[3]
            dev['usb_info'] = self.snmp_walk(
                dev['ip'], '1.3.6.1.2.1.8.1.3.0')
            for i in HOSTS:
                if i.ip == dev[ip]:
                    i.mesures['cpu_usage']['measures'].append((f'{current_time.hour}:{current_time.minute}',
                                                               dev['cpu_info']))
                    i.mesures['hdd_usage']['measures'].append((f'{current_time.hour}:{current_time.minute}',
                                                               dev['hdd_info']))
                    i.mesures['network_usage']['measures'].append((f'{current_time.hour}:{current_time.minute}',
                                                                   dev['network_info']))
                    i.hdd_total = dev['hdd_total']
                    i.status = dev['status']
                    i.usb_devs = dev['usb_info']

