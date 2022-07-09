import dataclasses
from typing import Optional, Sequence, Union

from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot, Message, Event, MessageSegment, MessageEvent, \
    GroupMessageEvent, NotifyEvent
from nonebot_plugin_pixivbot import context
from nonebot_plugin_pixivbot.postman import PostDestination as BasePostDestination, \
    PostDestinationFactory as BasePostDestinationFactory, PostIdentifier


class PostDestination(BasePostDestination[int, int, Bot, Message]):
    def __init__(self, bot: Bot, user_id: Optional[int] = None,
                 group_id: Optional[int] = None,
                 reply_to_message_id: Optional[int] = None):
        super().__init__(bot, PostIdentifier(user_id=user_id, group_id=group_id))
        self.reply_to_message_id = reply_to_message_id

    async def post(self, message: Union[Message, Sequence[Message]]):
        if len(message) == 0:
            logger.warning("message is empty")
        else:
            if isinstance(message[0], Message):
                if len(message) > 1:
                    await self.post_multiple(message)
                else:
                    await self.post_single(message[0])
            else:
                await self.post_single(message)

    async def post_single(self, message: Message):
        if self.reply_to_message_id:
            message.insert(0, MessageSegment.reply(self.reply_to_message_id))

        if self.group_id:
            await self.bot.send_group_msg(group_id=self.group_id, message=message)
        else:
            await self.bot.send_msg(user_id=self.user_id, message=message)

    async def post_multiple(self, messages: Sequence[Message]):
        if not self.group_id:
            for msg in messages:
                await self.post_single(msg)
        else:
            # 获取bot的群昵称
            self_info = await self.bot.get_group_member_info(group_id=self.group_id, user_id=self.bot.self_id)
            if self_info["card"]:
                nickname = self_info["card"]
            else:
                nickname = self_info["nickname"]

            # 创建转发消息
            msg_dict = []

            for msg in messages:
                msg_dict.append([dataclasses.asdict(seg) for seg in msg])

            messages = [{
                "type": "node",
                "data": {
                    "name": nickname,
                    "uin": self.bot.self_id,
                    "content": msg
                }
            } for msg in messages]

            await self.bot.send_group_forward_msg(
                group_id=self.group_id,
                messages=messages
            )


@context.register_singleton()
class PostDestinationFactory(BasePostDestinationFactory[int, int, Bot, Message]):
    def from_id(self, bot: Bot, identifier: PostIdentifier[int, int]) -> PostDestination:
        return PostDestination(bot, identifier.user_id, identifier.group_id)

    def from_message_event(self, bot: Bot, event: Event) -> PostDestination:
        if isinstance(event, MessageEvent) or isinstance(event, NotifyEvent):
            user_id = event.user_id
        else:
            user_id = None

        if isinstance(event, GroupMessageEvent) or isinstance(event, NotifyEvent):
            group_id = event.group_id
        else:
            group_id = None

        if isinstance(event, MessageEvent):
            reply_to_message_id = event.message_id
        else:
            reply_to_message_id = None

        return PostDestination(bot, user_id, group_id, reply_to_message_id)
