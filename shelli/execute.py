"""
Class for executing commands. Uses dependency injection
to run commands from a target.
"""

from shelli import authenticate
from shelli import transport

# Executor takes a target. The target contains all the information it needs to execute code
class Executor:
    """Class to manage executing commands on a host"""

    def __init__(self, target):
        """Nothing."""
        self.hosts = target.get_all_hosts()
        self.commands = target.commands
        self.transporters = []
        for transport_string in target.transports:
            self.transporters.append(transport.Transporter(transport_string))

    def execute(self):
        """Actually execute commands from a target onto its hosts"""

        # Get all connections. Will probably require authentication.
        # This way makes sure all hosts get authentication information up-front
        # Instead of 5 minutes later, after running a long command
        conns = []
        for cur_host in self.hosts.values():
            print("Creating connection {name}".format(name=cur_host.hostname))
            conns.append(authenticate.get_connection(cur_host))

        for conn in conns:
            # Transport any necessary files
            self.do_transport(conn)

            # Run commands
            for command in self.commands:
                conn.run(command)

            # Clean up, ya filthy animal
            self.cleanup(conn)

    def do_transport(self, connection):
        """Move files to remote"""
        for tranny in self.transporters:
            tranny.send(connection)

    def cleanup(self, connection):
        """Finish up stuff after remote execution"""
        for tranny in self.transporters:
            tranny.cleanup(connection)
