from os import getenv

API_ID = int(getenv("API_ID", 29400566))
API_HASH = str(getenv("API_HASH", "8fd30dc496aea7c14cf675f59b74ec6f"))
BOT_TOKEN = str(getenv("BOT_TOKEN", "7338403915:AAHGLDsHATKtooO_In7eCJsJujyvDQ-10mI"))
SUDOERS = list(map(int, getenv("SUDOERS", "6944434268 5746768920").split()))
