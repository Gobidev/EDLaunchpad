from EDSM import *
import Launchpad
import window

window.window()

if int(input("1=60sek refresh, 2=manual refresh\n")) == 1:

    if read_yaml("commander_name") == "key not found in config":
        settings()
    elif read_yaml("start_system") == "key not found in config":
        settings()
    elif read_yaml("end_system") == "key not found in config":
        settings()
    run()

else:
    Launchpad.button_press()
