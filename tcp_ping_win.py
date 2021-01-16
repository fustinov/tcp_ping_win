#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time
import argparse
import sys

# Input parameters
parser = argparse.ArgumentParser(description='This is a simple TCP ping for Windows')
parser.add_argument("--host", help="Destination host (IP or FQDN)", type=str, required=True)
parser.add_argument("-p", "--port", help="Destination port", type=int, required=True)
parser.add_argument("-n", "--number", help="Number of pings", type=int, default=4)
parser.add_argument("-w", "--wait", help="Frequency of the pings (in sec)", type=int, default=1)
parser.add_argument("-6", "--ipv6", help="Use IPv6 if available", action='store_true')

# Variables
remote_server = tuple()
args = parser.parse_args()
response_times = list()
resolved_address = list()

if args.ipv6:
    socket_type = socket.AF_INET6
else:
    socket_type = socket.AF_INET


# Basic functions
def findtime(start, end):
    return round(end - start, 3) * 1000


def check_port_arg(port):
    if (int(args.port) < 1) or (int(args.port) > 65535):
        print("Wrong port number. Please specify a correct one (1-65535)")
        sys.exit()
    return 0


def check_ip_addr(address, port):
    try:
        global resolved_address
        resolved_address = socket.getaddrinfo(address, port)
        if args.ipv6 and (len([addr6 for addr6 in resolved_address if 23 in addr6])) > 0:
            return 0
        elif args.ipv6 and (len([addr6 for addr6 in resolved_address if 23 in addr6])) == 0:
            print("The specified IP address either not an IPv6 address or DNS response did not contain any IPv6")
            print("Address(es): {}".format([addr6[4][0] for addr6 in resolved_address if 2 in addr6]))
            sys.exit()
        elif not args.ipv6 and (len([addr4 for addr4 in resolved_address if 2 in addr4])) == 0:
            print("No IPv4 specified or no IPv4 in DNS response")
            sys.exit()
        else:
            return 0
    except socket.gaierror:
        print("Invalid IP address or an issue with DNS resolution")
        sys.exit()


# Basic checks
check_port_arg(args.port)
check_ip_addr(args.host, args.port)
if args.ipv6:
    remote_server = [addr6 for addr6 in resolved_address if 23 in addr6][0][4]  # Use the first one
else:
    remote_server = [addr4 for addr4 in resolved_address if 2 in addr4][0][4]

# Main logic

for i in range(0, args.number):
    sock = socket.socket(socket_type, socket.SOCK_STREAM)
    init_time = time.time()
    try:
        sock.connect(remote_server)
        pass
    except OSError as err:
        if err.errno == 10060:
            print("Timeout, no response from the host {}".format(remote_server[0]))
            continue
        else:
            print("OS error: {0}".format(err))
            continue
    except:
        print("Unexpected error:", sys.exc_info()[0])
        continue

    end_time = time.time()
    sock.close()
    total_time = findtime(init_time, end_time)
    print('TCP connection with {} was established in {:g} msec'.format(remote_server[0], total_time))
    response_times.append(total_time)
    if i == args.number - 1:
        print('====================\nAverage handshake complete time was {:g} msec'.format(
            sum(response_times) // args.number))
        sys.exit()
    else:
        time.sleep(args.wait)
