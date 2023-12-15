from dataclasses import dataclass, field


@dataclass
class Host:
    interfaces: list = field(default_factory=list)
    hostname: str = field(default='[unknown]')
    status: str = field(default='[unknown]')
    system: str = field(default='[unknown]')


@dataclass
class Iface:
    address: str = field(default='[unknown]')
    status: str = field(default='[unknown]')

