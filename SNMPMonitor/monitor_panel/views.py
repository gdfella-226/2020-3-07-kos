from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from monitor_panel.models import Host
from loguru import logger
from monitor_panel.hosts import HOSTS


active_measure = 'hdd_usage'
active_host = HOSTS[0]
trouble_host = HOSTS[0]
show_warning = False


def index(request):
    global show_warning, trouble_host, active_host, active_measure

    if request.method == 'POST':
        if 'ip' in request.POST:
            active_host_ip = request.POST.get('ip')
            active_host = [i for i in HOSTS if i.ip == active_host_ip][0]

        if 'critical_value' in request.POST:
            active_host.measures[active_measure]['critical_value'] = int(request.POST.get('critical_value'))

    context = {
        'show_warning': show_warning,
        'trouble_host': trouble_host,
        'title': 'Host disconnected',
        'description': f'Connection with {trouble_host.hostname} has been lost',
        'hosts': HOSTS,
        'active_host': active_host
    }

    return render(request, 'index.html', context)


def get_chart_data(request):
    global active_host, active_measure
    labels = [pair[0] for pair in active_host.measures[active_measure]['measures']]
    values = [pair[1] for pair in active_host.measures[active_measure]['measures']]
    data = {
        'labels': labels,
        'values': values,
        'critical_value': active_host.measures[active_measure]['critical_value'],
    }
    return JsonResponse(data)


@csrf_exempt
def set_active_host(request):
    if request.method == 'POST':
        ip = request.POST.get('ip')
        saved_ip = ip
        return JsonResponse({'status': 'success', 'ip': saved_ip})
    return JsonResponse({'status': 'failed'})
