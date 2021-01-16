# Simple TCP ping script for Windows
This script is a basic implementation of ping over TCP. I tried to use only the standard Python library, so the script would only require Python 3 installed (tested on 3.6 and higher). 

## Usage

```
usage: tcp_ping_win.py [-h] --host HOST -p PORT [-n NUMBER] [-w WAIT] [-6]

This is a simple TCP ping for Windows

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           Destination host (IP or FQDN)
  -p PORT, --port PORT  Destination port
  -n NUMBER, --number NUMBER
                        Number of pings
  -w WAIT, --wait WAIT  Frequency of the pings (in sec)
  -6, --ipv6            Use IPv6 if available
```

## Examples
Example 1:
```
>tcp_ping_win.py --host 10.10.10.2 --port 443 -n 5 -w 3

TCP connection with 10.10.10.2 was established in 45 msec
TCP connection with 10.10.10.2 was established in 51 msec
TCP connection with 10.10.10.2 was established in 51 msec
TCP connection with 10.10.10.2 was established in 63 msec
TCP connection with 10.10.10.2 was established in 73 msec
====================
Average handshake complete time was 56.6 msec

```

Example 2:
```
tcp_ping_win.py --host www.google.com --port 443 -n 3 -6

TCP connection with 2a00:1450:401b:800::2004 was established in 31 msec
TCP connection with 2a00:1450:401b:800::2004 was established in 28 msec
TCP connection with 2a00:1450:401b:800::2004 was established in 21 msec
====================
Average handshake complete time was 26 msec

```