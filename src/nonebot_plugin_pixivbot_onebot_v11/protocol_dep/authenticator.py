from nonebot_plugin_pixivbot import context
from nonebot_plugin_pixivbot.protocol_dep.authenticator import Authenticator as BaseAuthenticator, \
    AuthenticatorManager

from nonebot_plugin_pixivbot_onebot_v11.protocol_dep.post_dest import PostDestination


@context.require(AuthenticatorManager).register
class Authenticator(BaseAuthenticator):
    @classmethod
    def adapter(cls) -> str:
        return "onebot"

    async def group_admin(self, post_dest: PostDestination) -> bool:
        result = await post_dest.bot.get_group_member_info(group_id=post_dest.group_id, user_id=post_dest.user_id)
        return result["role"] == "owner" or result["role"] == "admin"
