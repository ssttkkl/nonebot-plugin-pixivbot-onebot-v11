from typing import Dict, Type

from lazy import lazy
from nonebot import on_notice
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import PokeNotifyEvent
from nonebot_plugin_pixivbot import context
from nonebot_plugin_pixivbot.query import Query, DelegationQuery, RandomBookmarkQuery, \
    RandomRecommendedIllustQuery, RankingQuery, register_query

from nonebot_plugin_pixivbot_onebot_v11.config import OnebotV11Config


async def _group_poke(event: Event) -> bool:
    return isinstance(event, PokeNotifyEvent) and event.is_tome()


@register_query(context)
class PokeQuery(DelegationQuery):
    conf = context.require(OnebotV11Config)

    query_mapping: Dict[str, Type[Query]] = {
        "ranking": RankingQuery,
        "random_recommended_illust": RandomRecommendedIllustQuery,
        "random_bookmark": RandomBookmarkQuery
    }

    @lazy
    def matcher(self):
        return on_notice(_group_poke, priority=10, block=True)

    @lazy
    def delegation(self):
        query_type = self.query_mapping.get(self.conf.pixiv_poke_action)
        if query_type:
            return context.require(query_type)
        else:
            raise ValueError(f"invalid config: pixiv_poke_action={self.conf.pixiv_poke_action}")
