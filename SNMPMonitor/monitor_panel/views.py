from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from monitor_panel.models import Host
from loguru import logger
# from monitor_panel.core.SNMPManager import SNMPManager
# from monitor_panel.hosts import HOSTS
from monitor_panel.core.HostsScanner import HostsScanner

MANAGER = HostsScanner()
HOSTS = []
SHOW_WARNING = False


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        logger.info(HOSTS)
        context = super().get_context_data(**kwargs)
        active_measure = self.request.session.get('active_measure', 'cpu_usage')
        active_host_ip = self.request.session.get('active_host_ip', HOSTS[0].ip)
        active_host = [i for i in HOSTS if i.ip == active_host_ip][0]
        show_warning = self.request.session.get('show_warning', SHOW_WARNING)
        trouble_host = self.request.session.get('trouble_host', None)

        context.update({
            'show_warning': show_warning,
            'trouble_host': trouble_host,
            'title': 'Host disconnected',
            'description': f'Connection with {trouble_host.hostname} has been lost' if trouble_host else '',
            'hosts': HOSTS,
            'active_host': active_host,
            'active_measure': active_measure,
            'critical_value': active_host.measures[active_measure]['critical_value'],
        })
        logger.info(active_measure)
        return context

    def post(self, request, *args, **kwargs):
        if 'ip' in request.POST:
            active_host_ip = request.POST.get('ip')
            request.session['active_host_ip'] = active_host_ip
        if 'critical_value' in request.POST:
            active_measure = request.session.get('active_measure', 'cpu_usage')
            active_host_ip = request.session.get('active_host_ip', HOSTS[0].ip)
            active_host = next((i for i in HOSTS if i.ip == active_host_ip), HOSTS[0])
            active_host.measures[active_measure]['critical_value'] = int(request.POST.get('critical_value'))
        if 'warning' in request.POST:
            request.session['show_warning'] = request.POST.get('warning')

        return redirect('/dashboard')


@method_decorator(csrf_exempt, name='dispatch')
class GetChartDataView(View):
    def get(self, request, *args, **kwargs):
        active_measure = request.session.get('active_measure', 'cpu_usage')
        active_host_ip = request.session.get('active_host_ip', HOSTS[0].ip)
        active_host = next((i for i in HOSTS if i.ip == active_host_ip), HOSTS[0])
        labels = [pair[0] for pair in active_host.measures[active_measure]['measures']]
        values = [pair[1] for pair in active_host.measures[active_measure]['measures']]

        data = {
            'labels': labels,
            'values': values,
            'active_measure': active_measure,
            'critical_value': active_host.measures[active_measure]['critical_value'],
        }
        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class SetActiveHostView(View):
    def post(self, request, *args, **kwargs):
        if 'ip' in request.POST:
            ip = request.POST.get('ip')
            request.session['active_host_ip'] = ip
            return JsonResponse({'status': 'success', 'ip': ip})
        return JsonResponse({'status': 'failed'})


@method_decorator(csrf_exempt, name='dispatch')
class SetActiveMeasureView(View):
    def post(self, request, *args, **kwargs):
        if 'active_measure' in request.POST:
            request.session['active_measure'] = request.POST.get('active_measure')
            return redirect('/dashboard')
        return JsonResponse({'status': 'failed'})


@method_decorator(csrf_exempt, name='dispatch')
class RestartHost(View):
    def post(self, request, *args, **kwargs):
        ip = request.POST.get('ip')
        logger.info(ip)
        MANAGER.update_state(ip, 'status', 'Restarting')
        return JsonResponse({'status': 'success'})
        '''if MANAGER.manager.snmp_set(ip, '1.3.6.1.2.1.2.2.1.7.0', 2):
            if MANAGER.mng.check_devise(ip):
                return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'})'''


@method_decorator(csrf_exempt, name='dispatch')
class DisableIface(View):
    def post(self, request, *args, **kwargs):
        if MANAGER.manager.snmp_set(request.session.get(['active_host_ip']),
                                 '1.3.6.1.2.1.2.2.1.7.0', 2):
            if MANAGER.manager.snmp_set(request.session.get(['active_host_ip']),
                                 '1.3.6.1.2.1.2.2.1.7.0', 2):
                return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'})


class LoadHostsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'load.html')

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        host_generator = iter(MANAGER)
        try:
            host = next(host_generator)
            if host:
                HOSTS.append(host)
                return JsonResponse({'status': 'success', 'host': host.to_json()})
            else:
                return JsonResponse({'status': 'finished'})
        except StopIteration:
            return JsonResponse({'status': 'finished'})
