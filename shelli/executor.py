"""
Class for executing commands. Uses dependency injection
to run commands from a target.
"""

from getpass import getpass
from fabric import Connection

# Executor takes a target. The target contains all the information it needs to execute code
class Executor:
    """Class to manage executing commands on a host"""

    def __init__(self, target):
        """Nothing."""
        self.hosts = target.get_all_hosts()
        print(target.commands)
        self.commands = target.commands

    def transport(self):
        """Nothing."""

    def execute(self):
        """Actually execute commands from a target onto its hosts"""

        for host in self.hosts:
            password = getpass("Enter password for %s:" % host)
            conn = Connection(
                host.hostname,
                user=host.options['username'],
                port=host.options['port'],
                connect_kwargs={
                    'password': password
                }
            )
            for command in self.commands:
                print(command)
                conn.run(command)

    def cleanup(self):
        """Nothing."""
