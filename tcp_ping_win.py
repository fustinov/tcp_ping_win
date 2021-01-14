#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time 
import argparse
import ipaddress


#Input parameters
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='This is a simple TCP ping for Windows')
parser.add_argument("--host", help="Destination host", type=str)
parser.add_argument("-p", "--port", help="Destination port", type=int)
parser.add_argument("-n", "--number", help="Number of pings", type=int, default=4)


#Variables
remote_server = tuple()
args = parser.parse_args()

#Basic functions
def findtime(start, end):
	return round(end - start, 3)

def check_port_arg(port):
	if (int(args.port) <1) or (int(args.port) > 65535):
		print ("Wrong port number")
		return 1
	return 0

def check_ip_addr(address):
	try:
		address = '{}'.format(ipaddress.IPv4Address(address))
	except ipaddress.AddressValueError:
		print("Invalid IP address")
		return 1
	return 0

#Basic checks
check_port_arg(args.port)
check_ip_addr(args.host)

#Main logic
remote_server = (args.host,args.port)

for i in range(0,args.number):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	init_time = time.time()
	try:
		sock.connect(remote_server)
		pass
	except OSError as err:
		print("OS error: {0}".format(err))
		continue
	except:
		print("Unexpected error:", sys.exc_info()[0])
		continue

	end_time = time.time()
	sock.close()
	total_time = findtime(init_time, end_time)
	print('TCP connection with {} was established in {:.3f} sec'.format(args.host, total_time))
	time.sleep(1)