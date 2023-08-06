# https://github.com/wagtail/wagtail/blob/master/wagtail/utils/version.py
# This file is heavily inspired by django.utils.version
import subprocess

def get_version(version):
    """Return a PEP 440-compliant version number from VERSION."""
    version = get_complete_version(version)

    # Now build the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN - for pre-alpha releases
    #     | {a|b|rc}N - for alpha, beta, and rc releases

    main = get_main_version(version)

    sub = ''
    if version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'rc', 'dev': '.dev'}
        sub = mapping[version[3]] + str(version[4])

    return main + sub


def get_main_version(version=None):
    """Return main version (X.Y[.Z]) from VERSION."""
    version = get_complete_version(version)
    parts = 2 if version[2] == 0 else 3
    return '.'.join(str(x) for x in version[:parts])


def get_complete_version(version=None):
    """
    Return a tuple of the Wagtail version. If version argument is non-empty,
    check for correctness of the tuple provided.
    """
    if version is None:
        from wagtail import VERSION as version
    else:
        assert len(version) == 5
        assert version[3] in ('dev', 'alpha', 'beta', 'rc', 'final')

    return version


def get_semver_version(version):
    "Returns the semver version (X.Y.Z[-(alpha|beta)]) from VERSION"
    main = '.'.join(str(x) for x in version[:3])

    sub = ''
    if version[3] != 'final':
        sub = '-{}.{}'.format(*version[3:])
    return main + sub


def get_git_version():
    cmd = 'git describe --abbrev=0 --tags'.split()
    try:
        version = subprocess.check_output(cmd).decode().strip()
    except subprocess.CalledProcessError:
        print('Unable to get version number from git tags')
        version = None
    return version


def get_server_name():
    cmd = 'hostname'.split()
    try:
        hostname = subprocess.check_output(cmd).decode().strip()
    except subprocess.CalledProcessError:
        print('Unable to the name of the server')
        hostname = None
    return hostname
