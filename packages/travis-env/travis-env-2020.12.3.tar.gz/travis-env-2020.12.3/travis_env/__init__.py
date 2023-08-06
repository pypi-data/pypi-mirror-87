__all__ = ['vars', 'add', 'clear', 'delete', 'patch', 'update']


import os
import travis_env.api

"""
https://docs.travis-ci.com/api/#settings-environment-variables
"""


def vars(repo):
    ENDPOINT = os.getenv("TRAVIS_ENDPOINT", "https://api.travis-ci.org")
    url = "%s/repo/%s/env_vars" % (ENDPOINT, repo.replace("/", "%2F"))
    r = travis_env.api.request("GET", url)
    return {var["name"]: var["id"] for var in r.json()["env_vars"]}


def add(repo, var_name, var_value, public=False):
    """add environment variable"""
    ENDPOINT = os.getenv("TRAVIS_ENDPOINT", "https://api.travis-ci.org")
    data = {
        "env_var.name": var_name,
        "env_var.value": var_value,
        "env_var.public": public
    }
    url = "%s/repo/%s/env_vars" % (ENDPOINT, repo.replace("/", "%2F"))
    r = travis_env.api.request("POST", url, data)
    return r.json()


def patch(repo, var_id, var_value, public=None):
    """patch environment variable value"""
    ENDPOINT = os.getenv("TRAVIS_ENDPOINT", "https://api.travis-ci.org")
    data = {
        "env_var.value": var_value
    }
    if public is not None:
        data.update(public=public)
    url = "%s/repo/%s/env_var/%s" % (ENDPOINT,
                                     repo.replace("/", "%2F"), var_id)
    r = travis_env.api.request("PATCH", url, data)
    return r.json()


def update(repo, **kwargs):
    """update environment variable"""
    data = vars(repo)
    for var_name, var_value in kwargs.items():
        if var_name not in data:
            add(repo, var_name, var_value)
        else:
            var_id = data[var_name]
            patch(repo, var_id, var_value)


def delete(repo, var_name):
    """delete environment variable"""
    ENDPOINT = os.getenv("TRAVIS_ENDPOINT", "https://api.travis-ci.org")
    var_id = vars(repo).get(var_name, None)
    if var_id:
        url = "%s/repo/%s/env_var/%s" % (ENDPOINT,
                                         repo.replace("/", "%2F"), var_id)
        travis_env.api.request("DELETE", url)


def clear(repo):
    """clear all environment variables"""
    ENDPOINT = os.getenv("TRAVIS_ENDPOINT", "https://api.travis-ci.org")
    for var_name, var_id in vars(repo).items():
        url = "%s/repo/%s/env_var/%s" % (ENDPOINT,
                                         repo.replace("/", "%2F"), var_id)
        travis_env.api.request("DELETE", url)
