from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


trouble_host = '192.168.7.102'
show_warning = False
hosts = [
            {'ip': '192.168.7.101', 'name': 'HostName1', 'role': 'Manager', 'os': 'Ubuntu 2020.4',
             'status': 'Active', 'cpu_usage': 30, 'hdd_usage': 32, 'hdd_total': 50, 'network_usage': 50468, 'usb': 0},
            {'ip': '192.168.7.102', 'name': 'HostName2', 'role': 'Agent', 'os': 'Windows Server 2012',
             'status': 'Inactive', 'cpu_usage': 30, 'hdd_usage': 32, 'hdd_total': 100, 'network_usage': 9649, 'usb': 0},
            {'ip': '192.168.7.103', 'name': 'HostName3', 'role': 'Agent', 'os': 'Ubuntu Router',
             'status': 'Active', 'cpu_usage': 30, 'hdd_usage': 10, 'hdd_total': 30, 'network_usage': 2582542, 'usb': 2},
            {'ip': '192.168.7.104', 'name': 'HostName4', 'role': 'Agent', 'os': 'IPCam',
             'status': 'Active', 'cpu_usage': 30, 'hdd_usage': 32, 'hdd_total': 30, 'network_usage': 22684, 'usb': 0},
            {'ip': '192.168.7.105', 'name': 'HostName5', 'role': 'Agent', 'os': 'Windows 10',
             'status': 'Active', 'cpu_usage': 30, 'hdd_usage': 32, 'hdd_total': 50, 'network_usage': 5548, 'usb': 2},
        ]
active_host_ip = '192.168.7.101'
active_host = hosts[0]
critical_value = 75


def index(request):
    global show_warning, active_host_ip, trouble_host, hosts, active_host, critical_value

    if request.method == 'POST':
        if 'ip' in request.POST:
            active_host_ip = request.POST.get('ip')
            active_host = [i for i in hosts if i['ip'] == active_host_ip][0]
        if 'critical_value' in request.POST:
            critical_value = int(request.POST.get('critical_value'))

    context = {
        'show_warning': show_warning,
        'trouble_host': trouble_host,
        'title': 'Host disconnected',
        'description': f'Connection with {trouble_host} has been lost',
        'hosts': hosts,
        'active_host': active_host
    }

    return render(request, 'index.html', context)


def get_chart_data(request):
    global critical_value
    data = {
        'labels': ['12:35', '12:40', '12:45', '12:50', '12:55', '13:05', '13:10'],
        'values': [65, 59, 80, 81, 56, 55, 40],
        'critical_value': critical_value,
    }
    return JsonResponse(data)


@csrf_exempt
def set_active_host(request):
    global active_host_ip, show_warning
    if request.method == 'POST':
        ip = request.POST.get('ip')
        saved_ip = ip
        return JsonResponse({'status': 'success', 'ip': saved_ip})
    return JsonResponse({'status': 'failed'})