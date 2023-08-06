import json
from collections import OrderedDict
from datetime import datetime
import time
import os
from .basicChecks import bcolors


class checkConfig:
    def __init__(self, mode=""):
        local_config_folder = os.path.join(os.environ["HOME"], ".pydcer_config/")
        if os.path.isdir(local_config_folder):
            pass
        else:
            os.mkdir(local_config_folder)
        local_config_file = os.path.join(
            os.environ["HOME"], ".pydcer_config/pydcer_settings.json"
        )
        self.file_name = local_config_file
        self.mode = mode

    def getInfo(self):
        if self.mode == "force_change":
            return self.forceConfigChange()
        else:
            try:
                with open(self.file_name) as file_read_object:
                    pydcer_saved_config = json.load(file_read_object)
                    current_time = datetime.now()
                    config_saved_time = datetime.strptime(
                        pydcer_saved_config["time_stamp"], "%c"
                    )
                    difference_in_time = (current_time - config_saved_time)
                    if (difference_in_time.seconds + difference_in_time.days * 86400) >= 21600:
                        print(f'\n{bcolors.FAIL}{bcolors.BOLD}Look\'s like the stored config is 6 hour\'s old, so Please enter the below information{bcolors.ENDC}')
                        return self.forceConfigChange()
                    else:
                        return pydcer_saved_config
            except FileNotFoundError:
                return self.forceConfigChange()

    def forceConfigChange(self):
        subscription_name = input("\nPlease enter the subscription name:  ")
        default_path = input("\nPlease enter the path for the default directory where you have all your clones:  ")

        if os.name == "posix":
            path = os.sep
            for item in default_path.split(os.sep):
                if item != "":
                    path += item + os.sep
        elif os.name == "nt":
            path = os.sep
            items = default_path.split('/')
            for item in items:
                if item != "" and items.index(item) != 1:
                    path += item + os.sep
            path = items[1] + ":" + path
            
        pydcer_saved_config = OrderedDict()
        pydcer_saved_config["subscription"] = subscription_name
        pydcer_saved_config["path"] = path
        pydcer_saved_config["time_stamp"] = (datetime.now()).strftime("%c")

        pydcer_config_json = json.dumps(pydcer_saved_config)

        with open(self.file_name, "w") as file_write_object:
            file_write_object.write(pydcer_config_json)
        return pydcer_saved_config
