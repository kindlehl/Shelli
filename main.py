import conf
import host
import hostgroup

# Loads yml configuration. Without path argument, defaults to ~/.commander.yml
yaml = conf.YAMLoader(path='local.yml')
hosts = host.createHostsFromYaml(yaml)

print('printing host objects')

for h in hosts:
    print(h)

groups = hostgroup.createHostGroupsFromYaml(yaml)

for g in groups:
    print(g)
    for h in g.hosts:
        print(h)
        print(h.options)
