# ========= load nonebot_plugin_pixivbot =========
import nonebot

nonebot.load_plugin("nonebot_plugin_pixivbot")

# ================= provide beans =================
from nonebot_plugin_pixivbot import context

from .providers import *

provide(context)

# ================ register command ================
from .command import *
