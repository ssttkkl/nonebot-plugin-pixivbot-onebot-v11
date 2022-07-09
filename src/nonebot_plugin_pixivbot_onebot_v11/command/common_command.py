# import nonebot

from nonebot import on_regex, on_notice
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import PokeNotifyEvent
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nonebot_plugin_pixivbot import context
from nonebot_plugin_pixivbot.handler import *
from nonebot_plugin_pixivbot.postman import Postman
from nonebot_plugin_pixivbot.utils.config import Config

from nonebot_plugin_pixivbot_onebot_v11.postman import PostDestinationFactory
from .utils import get_count

conf = context.require(Config)
postman = context.require(Postman)
post_dest_factory = context.require(PostDestinationFactory)

if conf.pixiv_ranking_query_enabled:
    ranking_nth_query_handler = context.require(RankingHandler)

    mat = on_regex(r"^看看(.*)?榜\s*(.*)?$", priority=4, block=True)


    @mat.handle()
    async def handle_ranking_nth_query(bot: Bot, event: Event, state: T_State, matcher: Matcher):
        if "_matched_groups" in state:
            mode = state["_matched_groups"][0]
            num = state["_matched_groups"][1]
        else:
            mode = None
            num = None

        post_dest = post_dest_factory.from_message_event(bot, event)
        await ranking_nth_query_handler.handle(mode, num, post_dest=post_dest)

if conf.pixiv_illust_query_enabled:
    illust_query_handler = context.require(IllustHandler)

    mat = on_regex(r"^看看图\s*([1-9][0-9]*)$", priority=5)


    @mat.handle()
    async def handle_illust_query(bot: Bot, event: Event, state: T_State, matcher: Matcher):
        illust_id = state["_matched_groups"][0]

        post_dest = post_dest_factory.from_message_event(bot, event)
        await illust_query_handler.handle(illust_id, post_dest=post_dest)

if conf.pixiv_random_recommended_illust_query_enabled:
    random_recommended_illust_query_handler = context.require(RandomRecommendedIllustHandler)

    mat = on_regex("^来(.*)?张图$", priority=3, block=True)


    @mat.handle()
    async def handle_random_recommended_illust_query(bot: Bot, event: Event, state: T_State, matcher: Matcher):
        post_dest = post_dest_factory.from_message_event(bot, event)
        await random_recommended_illust_query_handler.handle(count=get_count(state), post_dest=post_dest)

if conf.pixiv_random_user_illust_query_enabled:
    random_user_illust_query_handler = context.require(RandomUserIllustHandler)

    mat = on_regex("^来(.*)?张(.+)老师的图$", priority=4, block=True)


    @mat.handle()
    async def handle_random_user_illust_query(bot: Bot, event: Event, state: T_State, matcher: Matcher):
        user = state["_matched_groups"][1]

        post_dest = post_dest_factory.from_message_event(bot, event)
        await random_user_illust_query_handler.handle(user, count=get_count(state), post_dest=post_dest)

if conf.pixiv_random_bookmark_query_enabled:
    random_bookmark_query_handler = context.require(RandomBookmarkHandler)

    mat = on_regex("^来(.*)?张私家车$", priority=5)


    @mat.handle()
    async def handle_random_bookmark_query(bot: Bot, event: Event, state: T_State, matcher: Matcher):
        post_dest = post_dest_factory.from_message_event(bot, event)
        await random_bookmark_query_handler.handle(count=get_count(state), post_dest=post_dest)

if conf.pixiv_random_illust_query_enabled:
    random_illust_query_handler = context.require(RandomIllustHandler)

    mat = on_regex("^来(.*)?张(.+)图$", priority=5)


    @mat.handle()
    async def handle_random_illust_query(bot: Bot, event: Event, state: T_State, matcher: Matcher):
        word = state["_matched_groups"][1]

        post_dest = post_dest_factory.from_message_event(bot, event)
        await random_illust_query_handler.handle(word, count=get_count(state), post_dest=post_dest)

if conf.pixiv_more_enabled:
    more_handler = context.require(MoreHandler)

    mat = on_regex("^还要$", priority=1, block=True)


    @mat.handle()
    async def handle_more(bot: Bot, event: Event, state: T_State, matcher: Matcher):
        post_dest = post_dest_factory.from_message_event(bot, event)
        await more_handler.handle(post_dest=post_dest)

if conf.pixiv_random_related_illust_query_enabled:
    random_related_illust_query_handler = context.require(RandomRelatedIllustHandler)

    mat = on_regex("^不够色$", priority=1, block=True)


    @mat.handle()
    async def handle_related_illust(bot: Bot, event: Event, state: T_State, matcher: Matcher):
        post_dest = post_dest_factory.from_message_event(bot, event)
        await random_related_illust_query_handler.handle(post_dest=post_dest)

if conf.pixiv_poke_action:
    handle_func = locals().get(f'handle_{conf.pixiv_poke_action}_query', None)
    if handle_func:
        async def _group_poke(event: Event) -> bool:
            return isinstance(event, PokeNotifyEvent) and event.is_tome()


        group_poke = on_notice(_group_poke, priority=10, block=True)
        group_poke.append_handler(handle_func)
    else:
        logger.warning(
            f"Bot will not respond to poke since {conf.pixiv_poke_action} is disabled.")
