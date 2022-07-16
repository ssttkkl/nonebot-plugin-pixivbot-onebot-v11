from nonebot import get_bot
from nonebot.adapters.onebot.v11 import Bot
from nonebot_plugin_pixivbot import context
from nonebot_plugin_pixivbot.handler.interceptor.permission_interceptor import \
    GroupAdminInterceptor as BaseGroupAdminInterceptor

from nonebot_plugin_pixivbot_onebot_v11.postman import PostDestination


@context.register_singleton()
class GroupAdminInterceptor(BaseGroupAdminInterceptor[int, int]):
    async def has_permission(self, post_dest: PostDestination) -> bool:
        if not post_dest.group_id:
            return True

        bot: Bot = get_bot()
        result = await bot.get_group_member_info(group_id=post_dest.group_id, user_id=post_dest.user_id)
        return result["role"] == "owner" or result["role"] == "admin"
