# ================= provide beans =================
from nonebot_plugin_pixivbot import context

from .providers import *

provide(context)

# ================ register command ================
from .command import *
