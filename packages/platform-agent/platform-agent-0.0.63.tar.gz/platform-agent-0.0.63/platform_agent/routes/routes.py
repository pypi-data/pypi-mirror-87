import logging
import socket

from pyroute2 import IPRoute, NetlinkError
from ipaddress import IPv4Network, ip_network

logger = logging.getLogger()


class Routes:
    def __init__(self):
        self.ip_route = IPRoute()

    def ip_route_add(self, ifname, ip_list, gw_ipv4):
        devices = self.ip_route.link_lookup(ifname=ifname)
        dev = devices[0]
        statuses = []
        routes = self.ip_route.get_routes(family=socket.AF_INET)
        network_list = []
        for route in routes:
            try:
                ip_cidr = (dict(route['attrs'])['RTA_DST'] + '/' + str(route['dst_len']))
                network_list.append(IPv4Network(ip_cidr))
            except (KeyError, ValueError):
                continue
        for ip in ip_list:
            # format ip to strict format
            formatted_ip = ip_network(ip, False)
            result = {'ip': ip, 'status': 'OK'}
            for network in network_list:
                if formatted_ip == network:
                    continue
                elif formatted_ip.overlaps(network):
                    result = {
                        'ip': ip,
                        'status': 'ERROR',
                        'msg': f'Service ip: {ip} intersects network CIDR {network}'
                    }
                    break
            if result['status'] == 'ERROR':
                statuses.append(result)
                continue
            try:
                self.ip_route.route('add', dst=formatted_ip.with_prefixlen, gateway=gw_ipv4, oif=dev)
            except NetlinkError as error:
                if error.code != 17:
                    result.update({'status': "ERROR", 'msg': str(error)})
                elif dict(self.ip_route.get_routes(dst=formatted_ip.with_prefixlen)[0]['attrs']).get('RTA_OIF') != dev:
                    logger.debug(f"[WG_CONF] add route failed [{ip}] - already exists")
                    result.update({'status': "ERROR", 'msg': "OVERLAP"})
            statuses.append(result)
        return statuses

    def ip_route_replace(self, ifname, ip_list, gw_ipv4):
        devices = self.ip_route.link_lookup(ifname=ifname)
        dev = devices[0]
        for ip in ip_list:
            try:
                self.ip_route.route('replace', dst=ip, gateway=gw_ipv4)
            except NetlinkError as error:
                if error.code != 17:
                    raise

    def ip_route_del(self, ifname, ip_list, scope=None):
        devices = self.ip_route.link_lookup(ifname=ifname)
        dev = devices[0]
        for ip in ip_list:
            try:
                self.ip_route.route('del', dst=ip, oif=dev, scope=scope)
            except NetlinkError as error:
                if error.code not in [17, 3]:
                    raise

    def create_rule(self, internal_ip, rt_table_id):
        self.ip_route.flush_rules(table=rt_table_id)
        self.ip_route.flush_routes(table=rt_table_id)
        self.ip_route.rule('add', src=internal_ip, table=rt_table_id)
