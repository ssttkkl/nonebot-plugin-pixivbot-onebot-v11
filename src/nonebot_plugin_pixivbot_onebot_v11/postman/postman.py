from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot_plugin_pixivbot import context
from nonebot_plugin_pixivbot.enums import BlockAction
from nonebot_plugin_pixivbot.postman import Postman as BasePostman
from nonebot_plugin_pixivbot.postman.model.illust_message import IllustMessageModel
from nonebot_plugin_pixivbot.postman.model.illust_messages import IllustMessagesModel

from nonebot_plugin_pixivbot_onebot_v11.postman.post_destination import PostDestination


@context.register_singleton()
class Postman(BasePostman[int, int]):

    @staticmethod
    def make_illust_msg(model: IllustMessageModel) -> Message:
        msg = Message()

        if model.block_action is not None:
            if model.block_action == BlockAction.no_image:
                msg.append(model.block_message)
            elif model.block_action == BlockAction.completely_block:
                msg.append(model.block_message)
                return msg
            elif model.block_action == BlockAction.no_reply:
                return msg
            else:
                raise ValueError(f"invalid block_action: {model.block_action}")

        msg.append(MessageSegment.image(model.image))

        if model.number is not None:
            msg.append(f"#{model.number}")
        msg.append(f"「{model.title}」\n"
                   f"作者：{model.author}\n"
                   f"发布时间：{model.create_time}\n"
                   f"{model.link}")
        return msg

    async def send_plain_text(self, message: str,
                              *, post_dest: PostDestination):
        message = Message([MessageSegment.text(message)])
        await post_dest.post(message)

    async def send_illust(self, model: IllustMessageModel,
                          *, post_dest: PostDestination):
        message = Message()
        if model.header is not None:
            message.append(MessageSegment.text(model.header))

        message.extend(self.make_illust_msg(model))
        await post_dest.post(message)

    async def send_illusts(self, model: IllustMessagesModel,
                           *, post_dest: PostDestination):
        if len(model.messages) == 1:
            await self.send_illust(model.flat_first(), post_dest=post_dest)
        else:
            messages = [Message([MessageSegment.text(model.header)])]
            for sub_model in model.messages:
                messages.append(self.make_illust_msg(sub_model))

            await post_dest.post(messages)


__all__ = ("Postman",)
