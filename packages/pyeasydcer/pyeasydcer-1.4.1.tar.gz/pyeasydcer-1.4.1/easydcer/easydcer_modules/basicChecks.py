import sys
import shutil
import os


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def checkForPython():
    if sys.version_info.major == 3:
        return True
    else:
        return False


def checkForLando():
    lando_location = shutil.which("lando")
    if lando_location is not None:
        return True
    else:
        return False


def checkForDrush():
    drush_location = shutil.which("drush")
    if drush_location is not None:
        return True
    else:
        return False


def basicChecks():
    print(f"\n{bcolors.WARNING}#######################{bcolors.ENDC}")
    print(f"\n{bcolors.WARNING}{bcolors.BOLD} Doing Initial checks {bcolors.ENDC}\n")
    python_check = checkForPython()
    print(f"{bcolors.WARNING} OS Type : {sys.platform}{bcolors.ENDC}")
    print(f"{bcolors.WARNING} Python3 Check : {str(python_check)}{bcolors.ENDC}")
    if "lando" in sys.argv:
        drush_check = checkForLando()
        print(f"{bcolors.WARNING} Lando Check : {str(drush_check)}{bcolors.ENDC}")
    else:
        drush_check = checkForDrush()
        print(f"{bcolors.WARNING} Drush Check : {str(drush_check)}{bcolors.ENDC}")
    print(f"\n{bcolors.WARNING}#######################{bcolors.ENDC}\n")
    if python_check and drush_check:
        return True
    else:
        return False


def rootCheck(path, subscription):
    destinationPath = (
        path + subscription + "/app/profiles/" + subscription + "_profile/content"
    )
    if os.path.isdir(path + subscription):
        if os.path.isdir(destinationPath):
            pass
        else:
            os.mkdir(destinationPath)
        return True
    else:
        return False


def checkForAvailableEntitiesText():
    local_config_folder = os.path.join(os.environ["HOME"], ".pydcer_config/")
    if os.path.isdir(local_config_folder):
        pass
    else:
        os.mkdir(local_config_folder)
    available_entities_config_file = os.path.join(
        os.environ["HOME"], ".pydcer_config/available_entities.txt"
    )
    if os.path.isfile(available_entities_config_file):
        return True
    else:
        with open(available_entities_config_file, "w") as write_object:
            available_entities_array = [
                "block_content",
                "node",
                "menu_link_content",
                "file",
                "config_pages",
                "taxonomy_term",
                "paragraphs",
                "user",
            ]
            for item in available_entities_array:
                write_object.write(item + "\n")
        return True
