from nonebot_plugin_pixivbot.context import Context

from .postman import providers as postman_providers
from .protocol_dep import providers as protocol_dep_providers


def provide(context: Context):
    postman_providers.provide(context)
    protocol_dep_providers.provide(context)


__all__ = ("provide",)
