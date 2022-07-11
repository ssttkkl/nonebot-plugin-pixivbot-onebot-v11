# import nonebot

from nonebot import on_regex, on_notice
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import PokeNotifyEvent
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nonebot_plugin_pixivbot import context
from nonebot_plugin_pixivbot.config import Config
from nonebot_plugin_pixivbot.handler import *
from nonebot_plugin_pixivbot.postman import Postman

from nonebot_plugin_pixivbot_onebot_v11.postman import PostDestinationFactory
from .utils import get_count

conf = context.require(Config)
postman = context.require(Postman)
post_dest_factory = context.require(PostDestinationFactory)

# ======== ranking_nth_query ========
ranking_nth_query_handler = context.require(RankingHandler)
if ranking_nth_query_handler.enabled():
    mat = on_regex(r"^看看(.*)?榜\s*(.*)?$", priority=4, block=True)


    @mat.handle()
    async def handle_ranking_nth_query(bot: Bot, event: Event, state: T_State, matcher: Matcher):
        if "_matched_groups" in state:
            mode = state["_matched_groups"][0]
            num = state["_matched_groups"][1]
        else:
            mode = None
            num = None

        post_dest = post_dest_factory.from_message_event(event)
        await ranking_nth_query_handler.handle(mode, num, post_dest=post_dest)

# ======== pixiv_illust_query ========
illust_query_handler = context.require(IllustHandler)
if illust_query_handler.enabled():
    mat = on_regex(r"^看看图\s*([1-9][0-9]*)$", priority=5)


    @mat.handle()
    async def handle_illust_query(bot: Bot, event: Event, state: T_State, matcher: Matcher):
        illust_id = state["_matched_groups"][0]

        post_dest = post_dest_factory.from_message_event(event)
        await illust_query_handler.handle(illust_id, post_dest=post_dest)

# ======== pixiv_random_recommended_illust_query ========
random_recommended_illust_query_handler = context.require(RandomRecommendedIllustHandler)
if random_recommended_illust_query_handler.enabled():
    mat = on_regex("^来(.*)?张图$", priority=3, block=True)


    @mat.handle()
    async def handle_random_recommended_illust_query(bot: Bot, event: Event, state: T_State, matcher: Matcher):
        post_dest = post_dest_factory.from_message_event(event)
        await random_recommended_illust_query_handler.handle(count=get_count(state), post_dest=post_dest)

# ======== random_user_illust_query ========
random_user_illust_query_handler = context.require(RandomUserIllustHandler)
if random_user_illust_query_handler.enabled():
    mat = on_regex("^来(.*)?张(.+)老师的图$", priority=4, block=True)


    @mat.handle()
    async def handle_random_user_illust_query(bot: Bot, event: Event, state: T_State, matcher: Matcher):
        user = state["_matched_groups"][1]

        post_dest = post_dest_factory.from_message_event(event)
        await random_user_illust_query_handler.handle(user, count=get_count(state), post_dest=post_dest)

# ======== random_bookmark_query ========
random_bookmark_query_handler = context.require(RandomBookmarkHandler)
if random_bookmark_query_handler.enabled():
    mat = on_regex("^来(.*)?张私家车$", priority=5)


    @mat.handle()
    async def handle_random_bookmark_query(bot: Bot, event: Event, state: T_State, matcher: Matcher):
        post_dest = post_dest_factory.from_message_event(event)
        await random_bookmark_query_handler.handle(count=get_count(state), post_dest=post_dest)

# ======== random_illust_query ========
random_illust_query_handler = context.require(RandomIllustHandler)
if random_illust_query_handler.enabled():
    mat = on_regex("^来(.*)?张(.+)图$", priority=5)


    @mat.handle()
    async def handle_random_illust_query(bot: Bot, event: Event, state: T_State, matcher: Matcher):
        word = state["_matched_groups"][1]

        post_dest = post_dest_factory.from_message_event(event)
        await random_illust_query_handler.handle(word, count=get_count(state), post_dest=post_dest)

# ======== more ========
more_handler = context.require(MoreHandler)
if more_handler.enabled():
    mat = on_regex("^还要((.*)张)?$", priority=1, block=True)


    @mat.handle()
    async def handle_more(bot: Bot, event: Event, state: T_State, matcher: Matcher):
        post_dest = post_dest_factory.from_message_event(event)
        await more_handler.handle(count=get_count(state, 1), post_dest=post_dest)

# ======== random_related_illust_query ========
random_related_illust_query_handler = context.require(RandomRelatedIllustHandler)
if random_related_illust_query_handler.enabled():
    mat = on_regex("^不够色$", priority=1, block=True)


    @mat.handle()
    async def handle_related_illust(bot: Bot, event: Event, state: T_State, matcher: Matcher):
        post_dest = post_dest_factory.from_message_event(event)
        await random_related_illust_query_handler.handle(post_dest=post_dest)

# ======== poke ========
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
