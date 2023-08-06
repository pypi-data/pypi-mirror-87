# ixconfig
Quick and simple `ifconfig` and `iwconfig` parsing.

## Install

```bash
pip install ixconfig
```

## Usage

```python
import ixconfig

# ifconfig

# returns an Ifc object - runs `ifconfig`
ifc = ixconfig.Ifc()
# which behaves like a dict
assert ifc['wlan0']['ip'] == "192.168.1.237"
# or an attrdict
assert ifc.wlan0.ip == "192.168.1.237"

# when you pass in an interface, it runs `ifconfig wlan0`
ifc = ixconfig.Ifc('wlan0')
# and then you can just access the attributes directly
assert ifc['ip'] == "192.168.1.237"
assert ifc.ip == "192.168.1.237"

# iwconfig

iwc = ixconfig.Iwc()
assert iwc['wlan0']['quality'] == 92.0
assert iwc.wlan0.quality == 92.0

iwc = ixconfig.Iwc('wlan0')
assert iwc['quality'] == 92.0
assert iwc.quality == 92.0

```

## Notes
This was code that I factored out of another project a while back. Eventually, I think this functionality should be covered `ifcfg`, but they don't handle `iwconfig` at the moment.

So until then, this package covers very basic parsing for both ifconfig and iwconfig.


## Example Outputs

```python

ifc = ixconfig.Ifc()
iwc = ixconfig.Iwc()
print(ifc)
print(iwc)
```

```python

( $ ifconfig ) {
    "docker0": {
        "broadcast": "172.17.255.255",
        "ip": "172.17.0.1",
        "ipv6": "fe80::42:f2ff:fe23:bb38",
        "mac": "02:42:f2:23:bb:38",
        "mtu": 1500,
        "name": "docker0",
        "netmask": "255.255.0.0",
        "rx_dropped": 0,
        "rx_errors": 0,
        "rx_overruns": 0,
        "rx_packets": 21326,
        "tx_carrier": 0,
        "tx_collisions": 0,
        "tx_dropped": 0,
        "tx_errors": 0,
        "tx_overruns": 0,
        "tx_packets": 30842
    },
    ...
    "wlan0": {
        "broadcast": "192.168.1.255",
        "ip": "192.168.1.237",
        "ipv6": "fe80::2998:5b3c:8ffb:a03d",
        "mac": "dc:a6:32:5d:df:ce",
        "mtu": 1500,
        "name": "wlan0",
        "netmask": "255.255.255.0",
        "rx_dropped": 0,
        "rx_errors": 0,
        "rx_overruns": 0,
        "rx_packets": 1960938,
        "tx_carrier": 0,
        "tx_collisions": 0,
        "tx_dropped": 0,
        "tx_errors": 0,
        "tx_overruns": 0,
        "tx_packets": 2790429
    }
}

( $ iwconfig ) {
    "wlan0": {
        "access_point": "A0:8E:78:59:45:D2",
        "bitrate": 72.2,
        "bitrate_unit": "Mb/s",
        "freq": 2.462,
        "freq_unit": "GHz",
        "mode": "Managed",
        "name": "wlan0",
        "power_mgmt": "on",
        "quality": 50.0,
        "quality_ratio": 0.7142857142857143,
        "ssid": "MySpectrumWiFicc-2G",
        "strength": -60.0,
        "strength_unit": "dBm"
    }
}

```
