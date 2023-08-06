#!/usr/bin/env python
"""delete environment variables by name"""
import travis_env
import click

MODULE_NAME = "travis_env.delete"
PROG_NAME = 'python -m %s' % MODULE_NAME
USAGE = 'python -m %s repo var_name ...' % MODULE_NAME


@click.command()
@click.argument('repo', required=True)
@click.argument('name', nargs=-1, required=True)
def _cli(repo, var_names):
    for var_name in var_names:
        travis_env.delete(var_name)


if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)
