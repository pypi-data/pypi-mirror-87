from invoke import Config, Program

from .tasks import deploy


class BuildtoolsConfig(Config):
    prefix = 'rbx'


program = Program(config_class=BuildtoolsConfig, namespace=deploy.ns, version='2.8.0.dev133')
