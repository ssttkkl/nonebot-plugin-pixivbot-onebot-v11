from nonebot_plugin_pixivbot.context import Context

from .protocol_dep import providers as protocol_dep_providers


def provide(context: Context):
    protocol_dep_providers.provide(context)


__all__ = ("provide",)
