import host
import copy

def createHostGroupsFromYaml(yaml):
    groups = []
    hosts = host.createHostsFromYaml(yaml)
    for groupyml in yaml['Hostgroups']:
        groupname = groupyml.keys()[0]
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
    def __init__(self, groupname, all_host_objects, yaml):
        self.name = groupname
        # names of all hosts in the group (might not be needed) IMMUTABLE
        self.hostnames =  yaml[groupname]['Hosts']
        if 'Options' in yaml[groupname].keys():
            self.options = copy.deepcopy(yaml[groupname]['Options'])
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
