from monitor_panel.models import Host

HOSTS = [
    Host(ip='192.168.7.101', hostname='Desktop-Manager', role='Manager', system='Ubuntu 2020.4', status='Active',
         hdd_total=50, usb_devs=0, measures={
            'cpu_usage': {
                'measures': [('12:35', 0), ('12:40', 30), ('12:45', 65), ('12:50', 65),
                             ('12:55', 65), ('13:05', 75), ('13:10', 20)],
                'critical_value': 70
            },
            'hdd_usage': {
                'measures': [('12:35', 30), ('12:40', 30), ('12:45', 31), ('12:50', 31),
                             ('12:55', 45), ('13:05', 30), ('13:10', 30)],
                'critical_value': 40
            },
            'network_usage': {
                'measures': [('12:35', 20987), ('12:40', 21087), ('12:45', 20987), ('12:50', 20987),
                             ('12:55', 20987), ('13:05', 22065), ('13:10', 35013)],
                'critical_value': 50000
            },
        }),
    Host(ip='192.168.7.102', hostname='Server', role='Agent', system='Windows Server 2016', status='Inactive',
         hdd_total=100, usb_devs=2, measures={
            'cpu_usage': {
                'measures': [('22:50', 0), ('22:55', 30), ('23:00', 70), ('23:05', 55),
                             ('23:10', 55), ('23:15', 75), ('23:20', 93)],
                'critical_value': 70
            },
            'hdd_usage': {
                'measures': [('12:35', 80), ('12:40', 80), ('12:45', 81), ('12:50', 50),
                             ('12:55', 50), ('13:05', 55), ('13:10', 55)],
                'critical_value': 40
            },
            'network_usage': {
                'measures': [('12:35', 20987), ('12:40', 21087), ('12:45', 20987), ('12:50', 20987),
                             ('12:55', 20987), ('13:05', 22065), ('13:10', 35013)],
                'critical_value': 50000
            },
        }),
    Host(ip='192.168.7.103', hostname='Desktop-J7V8BID4', role='Agent', system='Windows 10', status='Active',
         hdd_total=50, usb_devs=0, measures={
            'cpu_usage': {
                'measures': [('12:35', 0), ('12:40', 10), ('12:45', 10), ('12:50', 15),
                             ('12:55', 10), ('13:05', 10), ('13:10', 20)],
                'critical_value': 70
            },
            'hdd_usage': {
                'measures': [('12:35', 30), ('12:40', 30), ('12:45', 31), ('12:50', 31),
                             ('12:55', 31), ('13:05', 31), ('13:10', 31)],
                'critical_value': 40
            },
            'network_usage': {
                'measures': [('12:35', 20987), ('12:40', 21087), ('12:45', 20987), ('12:50', 20987),
                             ('12:55', 20987), ('13:05', 22065), ('13:10', 35013)],
                'critical_value': 50000
            },
        }),
    Host(ip='192.168.7.104', hostname='Router', role='Agent', system='RouterOS', status='Active',
         hdd_total=30, usb_devs=0, measures={
            'cpu_usage': {
                'measures': [('12:35', 0), ('12:40', 30), ('12:45', 35), ('12:50', 48),
                             ('12:55', 43), ('13:05', 15), ('13:10', 18)],
                'critical_value': 70
            },
            'hdd_usage': {
                'measures': [('12:35', 20), ('12:40', 20), ('12:45', 20), ('12:50', 20),
                             ('12:55', 20), ('13:05', 20), ('13:10', 20)],
                'critical_value': 25
            },
            'network_usage': {
                'measures': [('12:35', 20987), ('12:40', 21087), ('12:45', 20987), ('12:50', 20987),
                             ('12:55', 20987), ('13:05', 22065), ('13:10', 35013)],
                'critical_value': 50000
            },
        }),
    Host(ip='192.168.7.105', hostname='IPCam', role='Agent', system='Ubuntu 2020.4', status='Active',
         hdd_total=30, usb_devs=0, measures={
            'cpu_usage': {
                'measures': [('12:35', 0), ('12:40', 38), ('12:45', 35), ('12:50', 30),
                             ('12:55', 32), ('13:05', 30), ('13:10', 31)],
                'critical_value': 70
            },
            'hdd_usage': {
                'measures': [('12:35', 20), ('12:40', 20), ('12:45', 20), ('12:50', 20),
                             ('12:55', 20), ('13:05', 20), ('13:10', 20)],
                'critical_value': 25
            },
            'network_usage': {
                'measures': [('12:35', 20987), ('12:40', 21087), ('12:45', 20987), ('12:50', 20987),
                             ('12:55', 20987), ('13:05', 22065), ('13:10', 35013)],
                'critical_value': 50000
            },
        }),
]
