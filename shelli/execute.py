"""
Class for executing commands. Uses dependency injection
to run commands from a target.
"""

import sys
from multiprocessing import Process, Pipe

from shelli import authenticate
from shelli import logger
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
        connections = {}
        for cur_host in self.hosts.values():
            print("Creating connection {name}".format(name=cur_host))
            connections[str(cur_host)] = authenticate.get_connection(cur_host)

        threads = []
        # For each connection, spawn a thread and start it
        for hostname in connections:
           thread = Process(target=self.thread_execute, args=(hostname, connections[hostname]))
           thread.start()
           threads.append(thread)

        # Stall until all remote commands are done running
        for thread in threads:
            thread.join()

    def thread_execute(self, hostname, connection):
        # Transport any necessary files
        self.do_transport(connection)

        # Run commands
        self.run(hostname, self.commands, connection)

        # Clean up, ya filthy animal
        self.cleanup(connection)
        

    def run(self, message, commands, connection):
        """Runs a command on a given connection"""
        for command in commands:
            # Tell user what the heck is going on
            logger.report(message, "Running {}".format(command))

            # Run the command
            connection.run(command)

    def do_transport(self, connection):
        """Move files to remote"""
        for tranny in self.transporters:
            tranny.send(connection)

    def cleanup(self, connection):
        """Finish up stuff after remote execution"""
        for tranny in self.transporters:
            tranny.cleanup(connection)
