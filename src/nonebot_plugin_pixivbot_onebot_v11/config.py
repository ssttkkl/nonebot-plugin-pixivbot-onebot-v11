from typing import Optional

from nonebot import get_driver
from nonebot_plugin_pixivbot import context
from pydantic import validator, BaseSettings
from pydantic.fields import ModelField


@context.register_singleton(**get_driver().config.dict())
class OnebotV11Config(BaseSettings):
    pixiv_poke_action: Optional[str] = "random_recommended_illust"

    @validator('pixiv_poke_action')
    def pixiv_poke_action_validator(cls, v, field: ModelField):
        if v not in [None, "", "ranking", "random_recommended_illust", "random_bookmark"]:
            raise ValueError(f'illegal {field.name} value: {v}')
        return v

    class Config:
        extra = "ignore"


__all__ = ("OnebotV11Config",)
