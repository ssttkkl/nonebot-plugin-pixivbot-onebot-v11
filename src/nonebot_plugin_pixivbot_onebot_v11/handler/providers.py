from nonebot_plugin_pixivbot.context import Context
from nonebot_plugin_pixivbot.handler.interceptor.permission_interceptor import \
    GroupAdminInterceptor as BaseGroupAdminInterceptor

from .interceptor.permission_interceptor import GroupAdminInterceptor


def group_admin_interceptor_provider(context: Context):
    context.bind(BaseGroupAdminInterceptor, GroupAdminInterceptor)


providers = (group_admin_interceptor_provider,)

__all__ = ("providers",)
