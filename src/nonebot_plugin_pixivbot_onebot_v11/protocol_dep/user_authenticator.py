from nonebot import get_bot
from nonebot.adapters.onebot.v11 import Bot
from nonebot_plugin_pixivbot import context
from nonebot_plugin_pixivbot.protocol_dep.user_authenticator import UserAuthenticator as BaseUserAuthenticator

from nonebot_plugin_pixivbot_onebot_v11.postman import PostDestination


@context.bind_singleton_to(BaseUserAuthenticator)
class UserAuthenticator(BaseUserAuthenticator):
    async def group_admin(self, post_dest: PostDestination) -> bool:
        bot: Bot = get_bot()
        result = await bot.get_group_member_info(group_id=post_dest.group_id, user_id=post_dest.user_id)
        return result["role"] == "owner" or result["role"] == "admin"
