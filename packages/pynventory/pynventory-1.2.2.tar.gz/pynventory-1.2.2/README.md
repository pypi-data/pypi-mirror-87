**Pynventory**

Create a DokuWiki Linux Server inventory table.

```
# pynventory --help
usage: pynventory 192.168.1.0/24 --hostname --cpu_cores --memory

Create a DokuWiki friendly inventory table of you servers

positional arguments:
  ip_range      CIDR IP range. ie: 192.168.0.0/24

optional arguments:
  -h, --help    show this help message and exit
  --cpu_cores
  --hostname
  --os_version
  --ntp_host
  --memory
  --disk
  --kernel
  -d            enable verbose output to stderr
```