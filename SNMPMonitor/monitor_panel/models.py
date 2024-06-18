from django.db import models


class Host(models.Model):
    ip: list = models.GenericIPAddressField(protocol='IPv4', help_text='IP address of host`s network interface')
    hostname: str = models.CharField(max_length=20, help_text='Hostname')
    role: str = models.CharField(default='Agent', max_length=20, help_text='SNMP role: Manager / Agent')
    status: str = models.BooleanField(default=False, help_text='Device status: Active / Inactive')
    system: str = models.CharField(max_length=50, help_text='Name & version of host`s OS')
    hdd_total: int = models.IntegerField(default=50, help_text='Host`s HDD total spase (Gb')
    usb_devs: int = models.IntegerField(default=0, help_text='Amount of connected USB devices')
    measures: str = models.TextField(help_text='Collect measures of host`s parameters')

    def update_measures(self, param_val: tuple, critical) -> None:
        del self.measures[param_val[0]]['measures'][0]
        self.measures[param_val[0]]['measures'].append(param_val[1])
        measures[param_val[0]]['critical_value'] = critical

    def check_measures_for_crit(self) -> bool:
        for param in self.measures:
            crit = param['critical_value']
            for measure in param['measures']:
                if int(measure[1]) >= int(crit):
                    return True
        return False

    def to_json(self) -> dict:
        res = {
            'ip': self.ip,
            'hostname': self.hostname,
            'role': self.role,
            'status': self.status,
            'system': self.system,
            'hdd_total': self.system,
            'usb_devs': self.usb_devs,
            'measures': self.measures,
        }
        return res

