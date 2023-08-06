#!/usr/bin/env python
"""set environment variable"""
import travis_env
import click

MODULE_NAME = "travis_env.set"
PROG_NAME = 'python -m %s' % MODULE_NAME
USAGE = 'python -m %s repo var_name var_value' % MODULE_NAME


@click.command()
@click.argument('repo', required=True)
@click.argument('var_name', required=True)
@click.argument('var_value', required=True)
def _cli(repo, var_name, var_value):
    kwargs = {}
    kwargs[var_name] = var_value
    travis_env.update(repo, **kwargs)


if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)
