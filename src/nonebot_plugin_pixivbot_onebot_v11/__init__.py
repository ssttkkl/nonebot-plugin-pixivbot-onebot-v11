"""
nonebot-plugin-pixivbot-onebot-v11

@Author         : ssttkkl
@License        : MIT
@GitHub         : https://github.com/ssttkkl/nonebot-plugin-pixivbot-onebot-v11
"""

# ======= register Postman and PostDestination =======
from .postman import Postman, PostDestinationFactory

# =============== register protocol_dep ===============
from .protocol_dep.user_authenticator import UserAuthenticator

# ================== register query ==================
from .query import *
