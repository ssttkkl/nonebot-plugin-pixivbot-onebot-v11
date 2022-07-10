from asyncio import create_task
from io import BytesIO
from typing import Optional, Union, Sequence

from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment
from nonebot_plugin_pixivbot import context
from nonebot_plugin_pixivbot.data import PixivRepo
from nonebot_plugin_pixivbot.model import Illust
from nonebot_plugin_pixivbot.postman import Postman as BasePostman
from nonebot_plugin_pixivbot.utils.config import Config
from nonebot_plugin_pixivbot_onebot_v11.postman.post_destination import PostDestination


@context.register_singleton()
class Postman(BasePostman[int, int, Bot, Message]):
    conf = context.require(Config)
    repo = context.require(PixivRepo)

    async def make_illust_msg(self, illust: Illust,
                              number: Optional[int] = None) -> Message:
        msg = Message()

        if illust.has_tags(self.conf.pixiv_block_tags):
            if self.conf.pixiv_block_action == "no_image":
                msg.append("该画像因含有不可描述的tag而被自主规制\n")
            elif self.conf.pixiv_block_action == "completely_block":
                return Message(MessageSegment.text("该画像因含有不可描述的tag而被自主规制"))
            elif self.conf.pixiv_block_action == "no_reply":
                return Message()
        else:
            with BytesIO() as bio:
                bio.write(await self.repo.image(illust))
                msg.append(MessageSegment.image(bio))

        if number is not None:
            msg.append(f"#{number}")
        msg.append(f"「{illust.title}」\n"
                   f"作者：{illust.user.name}\n"
                   f"发布时间：{illust.create_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
                   f"https://www.pixiv.net/artworks/{illust.id}")
        return msg

    async def send_message(self, message: Union[str, Message],
                           *, post_dest: PostDestination):
        if isinstance(message, str):
            message = Message(message)
        await post_dest.post(message)

    async def send_illust(self, illust: Illust,
                          header: Union[str, Message, None] = None,
                          number: Optional[int] = None,
                          *, post_dest: PostDestination):
        message = Message()
        if header is not None:
            if header is str:
                message.append(MessageSegment.text(header))
            else:
                message.extend(header)

        message.extend(await self.make_illust_msg(illust, number))
        await post_dest.post(message)

    async def send_illusts(self, illusts: Sequence[Illust],
                           header: Union[str, Message, None] = None,
                           number: Optional[int] = None,
                           *, post_dest: PostDestination):
        if len(illusts) == 1:
            await self.send_illust(illusts[0], header, number, post_dest=post_dest)
        else:
            msg_fut = [create_task(self.make_illust_msg(illust, number + i if number is not None else None))
                       for i, illust in enumerate(illusts)]

            messages = [Message([MessageSegment.text(header)])]
            for fut in msg_fut:
                messages.append(await fut)

            await post_dest.post(messages)


__all__ = ("Postman",)
