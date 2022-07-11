import dataclasses
from typing import Optional, Sequence, Union

from nonebot import logger, get_bot
from nonebot.adapters.onebot.v11 import Bot, Message, Event, MessageSegment, MessageEvent, \
    GroupMessageEvent, NotifyEvent
from nonebot_plugin_pixivbot import context
from nonebot_plugin_pixivbot.postman import PostDestination as BasePostDestination, \
    PostDestinationFactory as BasePostDestinationFactory
from nonebot_plugin_pixivbot.postman.post_destination import GID, UID
from nonebot_plugin_pixivbot.utils.nonebot import get_adapter_name


class PostDestination(BasePostDestination[int, int]):
    def __init__(self, user_id: Optional[int] = None,
                 group_id: Optional[int] = None,
                 reply_to_message_id: Optional[int] = None):
        self._user_id = user_id
        self._group_id = group_id
        self.reply_to_message_id = reply_to_message_id

    @property
    def adapter(self) -> str:
        return get_adapter_name()

    @property
    def user_id(self) -> UID:
        return self._user_id

    @property
    def group_id(self) -> GID:
        return self._group_id

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
        bot = get_bot()

        if self.reply_to_message_id:
            message.insert(0, MessageSegment.reply(self.reply_to_message_id))

        if self.group_id:
            await bot.send_group_msg(group_id=self.group_id, message=message)
        else:
            await bot.send_msg(user_id=self.user_id, message=message)

    async def post_multiple(self, messages: Sequence[Message]):
        bot = get_bot()

        if not self.group_id:
            for msg in messages:
                await self.post_single(msg)
        else:
            # 获取bot的群昵称
            self_info = await bot.get_group_member_info(group_id=self.group_id, user_id=bot.self_id)
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
                    "uin": bot.self_id,
                    "content": msg
                }
            } for msg in messages]

            await bot.send_group_forward_msg(
                group_id=self.group_id,
                messages=messages
            )


@context.register_singleton()
class PostDestinationFactory(BasePostDestinationFactory[int, int]):
    def build(self, user_id: UID, group_id: GID) -> PostDestination:
        return PostDestination(user_id, group_id)

    def from_message_event(self, event: Event) -> PostDestination:
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

        return PostDestination(user_id, group_id, reply_to_message_id)
