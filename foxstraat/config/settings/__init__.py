from foxstraat.config.settings.base import *

try:
    from foxstraat.config.settings.production import *

except:
    from foxstraat.config.settings.local import *
