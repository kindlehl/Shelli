"""
Entry point for shelli cli
"""

from shelli import conf, target, cli_parser, execute

ARGS = cli_parser.get()

# Loads yml configuration. Without path argument, defaults to ~/.commander.yml
YAML = conf.YAMLoader(path=ARGS.config)
TARGETS = target.create_targets_from_yaml(YAML)

for t in TARGETS.values():
    if t.name == ARGS.target:
        runner = execute.Executor(t)
        runner.execute()
