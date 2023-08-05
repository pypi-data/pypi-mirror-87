psconfig-client is a python library to parse perfSONAR psconfig/PWA mesh configuration files 

```
Synopsis:
import psconfig.api
import logging
import sys

log = logging.getLogger()

if __name__ == '__main__':
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(message)s')
    fh = logging.StreamHandler(stream=sys.stdout)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    # url supports host auto-url, particular mesh or top level mesh directory
    # for https you can pass hostcert/key and verify flag, which are all passed to the requests library call
    x = psconfig.api.PSC('url', hostcert=None, hostkey=None, verify=False)
    # get all hosts from all groups
    print(x.get_all_hosts())
    # get all hosts from the group X
    print(x.get_hosts_by_group('X'))
    # get all hosts from the groups X, Y, Z
    print(x.get_hosts_by_group('X', 'Y', 'Z'))
    # get all hosts from all groups except A
    print(x.get_hosts_by_group(exclude='A'))

    # get test types (trace, throughput, latency, etc.) per host
    for h in x.get_hosts_by_group():
        print(h, x.get_test_types(h))
    
    # get site name of a host
    print(x.get_site('<hostname>')

    # get all hosts from the mesh configs X, Y, Z and not Q
    print(x.get_hosts_by_config('X', 'Y', 'Z', exclude='Q'))

```

