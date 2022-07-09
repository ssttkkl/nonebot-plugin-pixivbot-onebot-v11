from nonebot_plugin_pixivbot import context

from nonebot_plugin_pixivbot_onebot_v11.postman.providers import providers as postman_providers

providers = (*postman_providers,)

for p in providers:
    p(context)
