from raven import Client

from iris.core.plugins import Plugin


class SentryPlugin(Plugin):
    def __init__(self, container, dsn=None, **kwargs):
        self.container = container
        self.client = Client(dsn)
        self.container.error_hook.install(self.on_error)

    def on_error(self, exc_info):
        self.client.captureException(exc_info)
