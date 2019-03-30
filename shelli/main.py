from shelli import conf, target, cli_parser, remote_execution

args = cli_parser.get()

# Loads yml configuration. Without path argument, defaults to ~/.commander.yml
yaml = conf.YAMLoader()
targets = target.createTargetsFromYaml(yaml)

for t in targets:
    if t.name == args.target:
        runner = remote_execution.Executor(t)
        runner.execute()
