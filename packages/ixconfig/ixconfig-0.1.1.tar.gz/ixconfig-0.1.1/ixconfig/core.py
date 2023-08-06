import shlex
import fnmatch
import subprocess
from . import util
# import logging

# log = logging.getLogger(__name__)


class _BaseConfig(util.attrdict):
    PARAM_PATTERNS = []
    error_msgs = None

    def __init__(self, iface=None):
        self.iface = iface
        super().__init__()
        self.run()

    def __repr__(self):
        return super().__str__()

    def __str__(self):
        return '( $ {} ) {}'.format(self.cmd.strip(), super().__str__())

    @property
    def cmd(self):
        raise NotImplementedError()

    def _get_output(self):
        cmd = self.cmd
        return subprocess.check_output(
            shlex.split(cmd) if isinstance(cmd, str) else cmd,
            stderr=subprocess.STDOUT,
        ).decode('utf-8')

    def _process_results(self, result):
        return result

    def run(self):
        self.clear()
        out = self._get_output()
        if out:
            result = {
                d['name']: d for d in (
                    self._process_results(util.matchmany(o, self.PARAM_PATTERNS))
                    for o in util.split_indent(out)
                    if not any(
                        msg.lower() in o.lower()
                        for msg in util.as_tuple(self.error_msgs))
                )
            }
            self._full = result
            self.update(result.get(self.iface) or {} if self.iface else result)
        return self

    def __getitem__(self, key):
        get = super().__getitem__
        return (
            {k: get(k) for k in key}
            if isinstance(key, tuple) else
            get(key))

    def __getattr__(self, k):
        if k not in self:
            raise AttributeError(k)
        return self[k]

    @property
    def names(self):
        return (self.iface if self else None) if self.iface else list(self.keys())

    def select(self, *keys):
        return {k: self.get(k) for k in keys} if self.iface else {
            iface: {k: d.get(k) for k in keys}
            for iface, d in self.items()
        }

    def ifaces(self, *keys):
        return (
            (dict(self) if any(fnmatch.fnmatch(self.iface, k) or k in self.iface for k in keys) else None)
            if self.iface else {
            iface: d for iface, d in self.items()
            if any(fnmatch.fnmatch(iface, k) or k in iface for k in keys)
        })


class Ifc(_BaseConfig):
    '''
    wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
           inet 192.168.1.236  netmask 255.255.255.0  broadcast 192.168.1.255
           inet6 fe80::c082:c63f:7206:6148  prefixlen 64  scopeid 0x20<link>
           ether 74:da:38:5c:68:33  txqueuelen 1000  (Ethernet)
           RX packets 47295  bytes 6606945 (6.3 MiB)
           RX errors 0  dropped 0  overruns 0  frame 0
           TX packets 14509  bytes 2908876 (2.7 MiB)
           TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

    "wlan0": {
        "broadcast": "192.168.1.255",
        "ip": "192.168.1.237",
        "ipv6": "fe80::2998:5b3c:8ffb:a03d",
        "mac": "dc:a6:32:5d:df:ce",
        "mtu": "1500",
        "name": "wlan0",
        "netmask": "255.255.255.0",
        "rx_dropped": "0",
        "rx_errors": "0",
        "rx_overruns": "0",
        "rx_packets": "1960938",
        "tx_carrier": "0",
        "tx_collisions": "0",
        "tx_dropped": "0",
        "tx_errors": "0",
        "tx_overruns": "0",
        "tx_packets": "2790429"
    }
    '''
    PARAM_PATTERNS = [
        r'^(?P<name>\w+\d*):',
        r'mtu\s+(?P<mtu>[\d]+)',
        r'inet\s+(?P<ip>[\d.]+)',
        r'inet6\s+(?P<ipv6>[\w\d:%]+)',
        r'netmask\s+(?P<netmask>[\d.]+)',
        r'ether\s+(?P<mac>[\w\d:]+)',
        r'inet\s.+broadcast\s*(?P<broadcast>[\d.]+)',
        r'inet\s.+peer\s*(?P<tun_gw>[^\s]+)',
        r'RX packets\s*(?P<rx_packets>\d+)',
        r'RX errors\s*(?P<rx_errors>\d+)',
        r'RX .*dropped\s*(?P<rx_dropped>\d+)',
        r'RX .*overruns\s*(?P<rx_overruns>\d+)',
        r'TX packets\s*(?P<tx_packets>\d+)',
        r'TX errors\s*(?P<tx_errors>\d+)',
        r'TX .*dropped\s*(?P<tx_dropped>\d+)',
        r'TX .*overruns\s*(?P<tx_overruns>\d+)',
        r'TX .*carrier\s*(?P<tx_carrier>\d+)',
        r'TX .*collisions\s*(?P<tx_collisions>\d+)',
    ]
    error_msgs = ('device not found', 'does not exist')  # 'error',

    @property
    def cmd(self):
        return 'ifconfig {}'.format(self.iface or '')

    def _process_results(self, result):
        return util.maybe_cast(
            result, int,
            'mtu', 'rx_dropped', 'rx_errors', 'rx_overruns', 'rx_packets',
            'rx_dropped', 'rx_errors', 'rx_overruns', 'rx_packets',
            'tx_carrier', 'tx_collisions', 'tx_dropped', 'tx_errors',
            'tx_overruns', 'tx_packets')


class Iwc(_BaseConfig):
    '''

    Example Output:
        wlan0     IEEE 802.11  ESSID:"MySpectrumWiFicc-2G"
                  Mode:Managed  Frequency:2.462 GHz  Access Point: A0:8E:78:59:45:D2
                  Bit Rate=72.2 Mb/s   Tx-Power=20 dBm
                  Retry short limit:7   RTS thr=2347 B   Fragment thr:off
                  Power Management:off
                  Link Quality=70/70  Signal level=-40 dBm
                  Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
                  Tx excessive retries:0  Invalid misc:271   Missed beacon:0
    '''
    PARAM_PATTERNS = [
        r'^(?P<name>\w+\d+)',
        r'ESSID:"(?P<ssid>[^"]*)"',
        r'Mode:(?P<mode>[^\s]*)',
        r'Frequency:(?P<freq>[\d.]*)\s*(?P<freq_unit>\w*)',
        r'Access Point:\s*(?P<access_point>[\w\d:-]*)',
        r'Bit Rate=\s*(?P<bitrate>[\d.]*)\s*(?P<bitrate_unit>[\w\/]*)',
        r'Power Management:(?P<power_mgmt>\w*)',
        r'Link Quality=(?P<quality>[\d\/]+)',
        r'Signal level=(?P<strength>[-\d.]+)\s*(?P<strength_unit>\w+)',
        # r'Noise level=(?P<noise>[^\d.]*)',
        # r'Sensitivity:(?P<sensitivity>[^\s^\\N]*)',
        # r'Encryption key:(?P<enc_key>[^\s^\\N]*)',
    ]

    error_msgs = 'no such device', 'no wireless extensions'

    @property
    def cmd(self):
        return 'iwconfig {}'.format(self.iface or '')

    def _process_results(self, result):
        if 'quality' in result:
            qual, qualdenom = result['quality'].split('/')
            result['quality'] = float(qual)
            result['quality_ratio'] = result['quality'] / float(qualdenom)
        return util.maybe_cast(result, float, 'strength', 'freq', 'bitrate')


def ifcget(iface, *keys):
    return Ifc(iface).get(*keys)

def iwcget(iface, *keys):
    return Iwc(iface).get(*keys)
