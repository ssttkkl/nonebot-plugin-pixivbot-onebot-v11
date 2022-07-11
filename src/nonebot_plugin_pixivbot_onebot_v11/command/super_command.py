from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nonebot_plugin_pixivbot import context
from nonebot_plugin_pixivbot.handler import CommandHandler

from nonebot_plugin_pixivbot_onebot_v11.postman import PostDestinationFactory

mat = on_command("pixivbot", priority=5)
cmd_handler = context.require(CommandHandler)
post_dest_factory = context.require(PostDestinationFactory)


@mat.handle()
async def handle_super_command(bot: Bot, event: Event, state: T_State, matcher: Matcher):
    args = str(event.get_message()).strip().split()[1:]
    post_dest = post_dest_factory.from_message_event(event)
    await cmd_handler.handle(args, post_dest=post_dest)
