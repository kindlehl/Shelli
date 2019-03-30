"""
Implements a class to represent a group of hosts
and default authentication for all hosts within
the group. Individual host configuration will
overwrite the group settings. Also provides helper
methods such as loading groups from yaml.
"""

import copy
from shelli import host

def create_host_groups_from_yaml(yaml):
    """Loads groups into list from yaml passed in"""

    groups = []
    hosts = host.create_hosts_from_yaml(yaml)
    for groupyml in yaml['hostgroups']:
        groupname = list(groupyml.keys())[0]
        groups.append(HostGroup(groupname, hosts, groupyml))
    return groups

# Valid YAML exerpt
#
# Hostgroups:
#   - DNS:        <------- You are passed this part
#       Hosts:
#         - ns1
#         - ns2
#       Options:
#         auth_method: PSK
#         auth_secret: 'Insecure as fuck'
#
#
# python representation -> [{'DNS': {'Hosts': ['ns1','ns2']}}]

class HostGroup:
    """Class for creating a hostgroup from yaml."""

    def __init__(self, groupname, all_host_objects, yaml):
        self.name = groupname
        # names of all hosts in the group (might not be needed) IMMUTABLE
        self.hostnames = yaml[groupname]['hosts']
        if 'Options' in list(yaml[groupname].keys()):
            self.options = copy.deepcopy(yaml[groupname]['options'])
        else:
            self.options = {}
        self.hosts = []
        for host_object in all_host_objects:
            if host_object.hostname in self.hostnames:
                # copy host object
                new_host = copy.deepcopy(host_object)
                # save options passed to host in yml configuration
                new_host_original_options = copy.deepcopy(new_host.options)
                # change the host's options to the group defaults
                new_host.options = copy.deepcopy(self.options)

                # Merge host-specific options into group defaults
                # semantically, this means that the group defaults will be applied, but the
                # host-specific options will stick
                new_host.options.update(new_host_original_options)
                self.hosts.append(new_host)

    def __str__(self):
        return self.name

    def __repl__(self):
        return str(self)
