"""
Entry point for shelli cli
"""

from shelli import conf, target, cli_parser, executor

ARGS = cli_parser.get()

# Loads yml configuration. Without path argument, defaults to ~/.commander.yml
YAML = conf.YAMLoader()
TARGETS = target.create_targets_from_yaml(YAML)

for t in TARGETS:
    if t.name == ARGS.target:
        runner = executor.Executor(t)
        runner.execute()
