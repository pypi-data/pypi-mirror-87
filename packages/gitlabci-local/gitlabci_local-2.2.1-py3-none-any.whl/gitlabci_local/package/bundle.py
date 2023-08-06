#!/usr/bin/env python3

# Bundle class
class Bundle:

    # Aliases
    ALIAS = 'gcil'

    # Names
    NAME = 'gitlabci-local'

    # Configurations
    CONFIGURATION = '.gitlab-ci.yml'

    # Sources
    REPOSITORY = 'https://gitlab.com/AdrianDC/gitlabci-local'

    # Environment
    ENV_ENGINE = 'CI_LOCAL_ENGINE'
    ENV_UPDATES_DISABLE = 'CI_LOCAL_UPDATES_DISABLE'
    ENV_UPDATES_OFFLINE = 'CI_LOCAL_UPDATES_OFFLINE'
    ENV_WINPTY = 'CI_LOCAL_WINPTY'
