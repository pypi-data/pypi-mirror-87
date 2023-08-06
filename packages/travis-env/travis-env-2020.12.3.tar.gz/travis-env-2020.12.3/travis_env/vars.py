#!/usr/bin/env python
"""print environment variable names"""
import travis_env
import click

MODULE_NAME = "travis_env.vars"
PROG_NAME = 'python -m %s' % MODULE_NAME
USAGE = 'python -m %s repo' % MODULE_NAME


@click.command()
@click.argument('repo', required=True)
def _cli(repo):
    vars = travis_env.vars(repo)
    if vars:
        names = vars.keys()
        print("\n".join(sorted(names)))


if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)
