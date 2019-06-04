from EDSM import *
import window

if read_yaml("commander_name") == "key not found in config":
    settings()
elif read_yaml("start_system") == "key not found in config":
    settings()
elif read_yaml("end_system") == "key not found in config":
    settings()

window.window()

try:
    import Launchpad
    run()
except:
    pass
