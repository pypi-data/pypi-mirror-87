import sys
import argparse
import ipaddress
import threading

from queue import Queue
import socket

import paramiko

from pynventory.hosts import LinuxHost


parser = argparse.ArgumentParser(description='Create a DokuWiki friendly inventory table of you servers',
                                 usage='pynventory 192.168.1.0/24 --hostname --cpu_cores --memory')
parser.add_argument('ip_range', action='store', help='CIDR IP range. ie: 192.168.0.0/24')
parser.add_argument('--cpu_cores', action='append_const', const=LinuxHost.GetCpuCores, dest='host_checks')
parser.add_argument('--hostname', action='append_const', const=LinuxHost.GetHostname, dest='host_checks')
parser.add_argument('--os_version', action='append_const', const=LinuxHost.GetOsRelease, dest='host_checks')
parser.add_argument('--ntp_host', action='append_const', const=LinuxHost.GetNtpServer, dest='host_checks')
parser.add_argument('--memory', action='append_const', const=LinuxHost.GetMemory, dest='host_checks')
parser.add_argument('--disk', action='append_const', const=LinuxHost.GetDiskSize, dest='host_checks')
parser.add_argument('--kernel', action='append_const', const=LinuxHost.GetKernelVersion, dest='host_checks')
parser.add_argument('--link_host',
                    action='store',
                    dest='link_host',
                    default=False,
                    help='create link to a new page for host description with this as base url')
parser.add_argument('--link_empty_host',
                    action='store_true',
                    default=False,
                    help='create links for nonexistent hosts')
parser.add_argument('--user', action='store', dest='ssh_user', help='ssh user', default='root')
parser.add_argument('--report_errors',
                    action='store_true',
                    dest='report_errors',
                    help='Report connection failures (except for timeout) to stdout')
parser.add_argument('-d', action='store_true', dest='debug', help='enable verbose output to stderr')
args = parser.parse_args()

# Defining globals
# Creating queue
compress_queue = Queue()
# Main result list.
result = []


def check_host(host):
    if not args.debug:
        print('.', end='', file=sys.stderr, flush=True)

    try:
        i = LinuxHost(host, args.ssh_user)
        host_result = [i, ]
        for check in args.host_checks:
            host_result.append(check(i))

        if args.debug:
            print('Host: %s Ok' % host, file=sys.stderr)

    except paramiko.ssh_exception.NoValidConnectionsError as e:
        # NoValidConnection wraps all socket related exceptions socket.error
        empty_list = ['' for _ in range(len(args.host_checks))]
        if args.report_errors:
            empty_list[0] = 'Error: ' + ' '.join(str(e).split()[2:8])
        host_result = [host, ] + empty_list

    except socket.timeout as e:
        # Don't report socket timeouts
        empty_list = ['' for _ in range(len(args.host_checks))]

        host_result = [host, ] + empty_list
        if args.debug:
            print('Host: %s Error: %s' % (host, e), file=sys.stderr)

    except (paramiko.ssh_exception.AuthenticationException, Exception) as e:
        # Catch all paramiko Auth exceptions
        empty_list = ['' for _ in range(len(args.host_checks))]
        if args.report_errors:
            empty_list[0] = 'Error: ' + str(e)
        host_result = [host, ] + empty_list

    finally:
        result.append(host_result)

    return


def process_queue():
    while True:
        host_data = compress_queue.get()
        check_host(host_data)
        compress_queue.task_done()


def main():
    # Exit if no checks are given
    if not args.host_checks:
        parser.print_help()
        exit(1)

    # Starting threads
    threads = 10
    for _ in range(threads):
        t = threading.Thread(target=process_queue)
        t.daemon = True
        t.start()

    # Providing threads with work
    ip_range = ipaddress.ip_network(args.ip_range)
    # Ignore Network and Broadcast addresses
    skipp_addresses = [ip_range.network_address, ip_range.broadcast_address]
    for host in ip_range:
        if host in skipp_addresses:
            continue
        compress_queue.put(str(host))

    # Wait for queue to finish
    compress_queue.join()

    # Force a clean line break before output
    print(file=sys.stderr)

    # Results from queues are not sorted.
    host_result = sorted(result[1:], key=lambda a: int(str(a[0]).split('.')[3]))

    header_title = ['Host', ] + [check.display_name() for check in args.host_checks]

    # Convert all the cells into strings
    cells = [[str(cell) for cell in row] for row in [header_title, ] + host_result]

    # create link to hosts if arg is set
    if args.link_host:
        for row in cells[1:]:
            # Only create a link if the host exists or the flag is set
            if row[1] or args.link_empty_host:
                row[0] = f'[[{args.link_host}:{row[0]}|{row[0]}]]'

    # Get longest entry for every column
    column_length = [max(map(len, col)) for col in zip(*cells)]

    # Create spacing for cells
    format_header = '^ {} ^'.format(' ^ '.join('{{:{}}}'.format(length) for length in column_length))
    format_body = '| {} |'.format(' | '.join('{{:{}}}'.format(length) for length in column_length))

    # Print output...
    print(format_header.format(*header_title))

    for row in cells[1:]:
        print(format_body.format(*row))


if __name__ == '__main__':
    main()
