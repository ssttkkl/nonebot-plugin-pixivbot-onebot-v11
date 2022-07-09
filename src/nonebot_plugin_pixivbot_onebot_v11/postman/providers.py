from nonebot_plugin_pixivbot.postman import Postman as BasePostman, PostDestinationFactory as BasePostDestinationFactory
from nonebot_plugin_pixivbot.utils.context import Context

from nonebot_plugin_pixivbot_onebot_v11.postman import Postman, PostDestinationFactory


def postman_provider(context: Context):
    context.bind(BasePostman, Postman)


def post_destination_factory_provider(context: Context):
    context.bind(BasePostDestinationFactory, PostDestinationFactory)


providers = (postman_provider, post_destination_factory_provider)

__all__ = ("providers",)
