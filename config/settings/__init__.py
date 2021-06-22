from config.settings.base import *

try:
    from config.settings.production import *

except:
    from config.settings.local import *