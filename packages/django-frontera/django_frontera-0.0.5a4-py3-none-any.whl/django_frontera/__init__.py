from django_frontera.contrib.utils.version import get_semver_version, get_version

# dev
# alpha
# beta
# rc
# final
# VERSION = (0, 0, 5, 'dev', 1)
VERSION = (0, 0, 5, 'alpha', 4)

__version__ = get_version(VERSION)

# Required for npm package for frontend
__semver__ = get_semver_version(VERSION)