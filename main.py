import conf
import target

# Loads yml configuration. Without path argument, defaults to ~/.commander.yml
yaml = conf.YAMLoader(path='local.yml')

print('printing target objects')

targets = target.createTargetsFromYaml(yaml)

for t in targets:
    print(dir(t))
    print(t.name)
    for g in t.hostgroups:
        print(g)
        for h in g.hosts:
            print(h)
            print(h.options)
