from nonebot_plugin_pixivbot.context import Context
from nonebot_plugin_pixivbot.protocol_dep import UserAuthenticator as BaseUserAuthenticator

from .user_authenticator import UserAuthenticator


def user_authenticator_provider(context: Context):
    context.bind(BaseUserAuthenticator, UserAuthenticator)


providers = (user_authenticator_provider,)


def provide(context: Context):
    for p in providers:
        p(context)


__all__ = ("provide",)
