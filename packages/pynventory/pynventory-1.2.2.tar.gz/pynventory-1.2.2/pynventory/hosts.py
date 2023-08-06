from fabric import Connection
from invoke.exceptions import UnexpectedExit


class LinuxHost:
    def __init__(self, host, user):
        self.connection = Connection(host, connect_timeout=1, user=user, connect_kwargs={'passphrase': 'Bv$2qu@t13'})
        self.host = host

    @staticmethod
    def display_name():
        return 'Host'

    def __str__(self):
        return self.host

    class GetOsRelease:
        def __init__(self, parent):
            try:
                self.output = parent.connection.run('cat /etc/os-release | grep "PRETTY_NAME"', hide=True)
                self.output = self.output.stdout.split('=')[1].replace('"', '')
            except UnexpectedExit:
                try:
                    self.output = parent.connection.run(' cat /etc/redhat-release', hide=True)
                    self.output = self.output.stdout
                except UnexpectedExit:
                    self.output = "Failed to retrieve OS Release"

        def __str__(self):
            # some words to remove from output as they are redundant
            clean_up = ['Linux', 'Server', 'release']
            _out = []

            for i in self.output.split():
                if i not in clean_up:
                    _out.append(i)
            return ' '.join(_out)

        @staticmethod
        def display_name():
            return 'OS Version'

    class GetHostname:
        def __init__(self, parent):
            self.output = parent.connection.run('hostname', hide=True).stdout

        @staticmethod
        def display_name():
            return 'Hostname'

        def __str__(self):
            return self.output.strip()

    class GetNtpServer:
        def __init__(self, parent):
            output = parent.connection.run('ntpq -pn', hide=True)
            # ntpq will output error if daemon is not running
            if output.stderr:
                self.output = [output.stderr.strip(), ]
            else:
                # remove header from ntpq output
                self.output = output.stdout.strip().split('\n')[2:]

        def __str__(self):
            # Filter out details and only return server ip
            servers = []
            for line in self.output:
                servers.append(line.split(' ')[0])
            return ', '.join(servers)

        @staticmethod
        def display_name():
            return 'NTP Server'

    class GetCpuCores:
        def __init__(self, parent):
            self.output = parent.connection.run('nproc', hide=True).stdout

        def __str__(self):
            return self.output.strip()

        @staticmethod
        def display_name():
            return 'Core count'

    class GetMemory:
        def __init__(self, parent):
            output = parent.connection.run('free -h', hide=True).stdout
            # Split output into lines, then split the columns and take total memory value
            self.memory = output.split('\n')[1].split()[1]

        def __str__(self):
            return self.memory

        @staticmethod
        def display_name():
            return 'Memory'

    class GetDiskSize:
        def __init__(self, parent):
            output = parent.connection.run('df -h -l --total', hide=True).stdout
            # Split output into lines, then split the columns and take disk size
            self.disk_size = output.split('\n')[-2].split()[1]

        def __str__(self):
            return self.disk_size

        @staticmethod
        def display_name():
            return 'Disk size'

    class GetKernelVersion:
        def __init__(self, parent):
            self.output = parent.connection.run('uname -r', hide=True).stdout

        def __str__(self):
            return self.output.strip()

        @staticmethod
        def display_name():
            return 'Kernel version'
