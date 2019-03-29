import copy
import hostgroup

# Valid yml exerpt
# targets:
#   touch:      <------------- You get this
#     commands:
#       - touch /home/kindlehl/testingcommander
#     groups:
#       - DNS

# Targets are READ ONLY
# Do NOT modify anything in them. This way, you won't need to make copies of everything!!!
class Target:
    def __init__(self, name, all_hostgroups, target_yaml):
        self.name = name
        self.commands = target_yaml['commands']
        self.hostgroup_names = target_yaml['hostgroups']
        self.transports = []
        if 'transport' in target_yaml.keys():
            self.transports = target_yaml['transport']

        self.hostgroups = []
        for group in all_hostgroups:
            if group.name in self.hostgroup_names:
                self.hostgroups.append(group)

    def __str__(self):
        return self.name

    def __repl__(self):
        return str(self)


def createTargetsFromYaml(yaml):
    all_hostgroups = hostgroup.createHostGroupsFromYaml(yaml)
    targets = []
    for target in yaml['targets']:
        target_name = target.keys()[0]
        new_target = Target(target_name, all_hostgroups, target) 
        targets.append(new_target)
    return targets
