import dataclasses
from typing import Optional, Sequence, Union

from nonebot import logger, get_bot
from nonebot.adapters.onebot.v11 import Message, Event, MessageSegment
from nonebot_plugin_pixivbot import context
from nonebot_plugin_pixivbot.postman import PostDestination as BasePostDestination, \
    PostDestinationFactory as BasePostDestinationFactory, PostDestinationFactoryManager
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
    def user_id(self) -> Optional[int]:
        return self._user_id

    @property
    def group_id(self) -> Optional[int]:
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


@context.require(PostDestinationFactoryManager).register
class PostDestinationFactory(BasePostDestinationFactory[int, int]):
    @classmethod
    def adapter(cls) -> str:
        return "onebot"

    def build(self, user_id: Optional[int], group_id: Optional[int]) -> PostDestination:
        return PostDestination(user_id, group_id)

    def from_event(self, event: Event) -> PostDestination:
        user_id = getattr(event, "user_id", None)
        group_id = getattr(event, "group_id", None)
        reply_to_message_id = getattr(event, "message_id", None)

        if not user_id and not group_id:
            raise ValueError("user_id 和 group_id 不能同时为 None")

        return PostDestination(user_id, group_id, reply_to_message_id)
