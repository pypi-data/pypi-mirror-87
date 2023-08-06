#!/usr/bin/env python
import sys
import os
import json
from datetime import datetime
from easydcer_modules import config, basicChecks, dcer

bcolors = basicChecks.bcolors
subscription = ""
base_path = ""
entity_type = ""


def usage():
    print(f"\n{bcolors.WARNING}Usage:{bcolors.ENDC} {bcolors.FAIL}pyeasydcer <entity_type> <id's of entities separated by a comma(,){bcolors.ENDC}")
    print(f"\n{bcolors.WARNING}A Python script to automate default content export in Drupal.{bcolors.ENDC}")
    print(f"\n{bcolors.WARNING}This script stores subscription and path in a config file so as user does not need to type them everytime they use the script for the next 6 hours{bcolors.ENDC}")
    print(f"\n{bcolors.WARNING}When the script asks for user input, it asks for subscription name and path where the root of the project is located{bcolors.ENDC}")
    print(f"\n\t{bcolors.OKGREEN}For *NIX OS users, if for example the project is located at{bcolors.ENDC} {bcolors.FAIL}/Users/vrvik/Sites/pfexportme{bcolors.ENDC}, {bcolors.OKGREEN}then path the user need to enter when asked is {bcolors.FAIL}/Users/vrvik/Sites{bcolors.ENDC}")
    print(f"\n\t{bcolors.OKGREEN}For Windows OS users, if for example the project is located at{bcolors.ENDC} {bcolors.FAIL}/d/xampp/htdocs/pfexportme{bcolors.ENDC}, {bcolors.OKGREEN}then path the user need to enter when asked is {bcolors.FAIL}/d/xampp/htdocs{bcolors.ENDC}")
    print(f"\n{bcolors.WARNING}Positional arguments:{bcolors.ENDC}")
    print(f"\t{bcolors.FAIL}There are no positional arguments for this script{bcolors.ENDC}\n\t{bcolors.WARNING}User can use arguments in any combination without worrying about the order in which arguments are given{bcolors.ENDC}")
    print(f"\n{bcolors.WARNING}Optional arguments:{bcolors.ENDC}")
    print(f"\t{bcolors.FAIL}lando{bcolors.ENDC}   {bcolors.WARNING}If you are using a lando environment use lando argument{bcolors.ENDC}")
    print(f"\t{bcolors.FAIL}-force{bcolors.ENDC}   {bcolors.WARNING}Force change configuration stored by script{bcolors.ENDC}")
    print(f"\t{bcolors.FAIL}-config{bcolors.ENDC}   {bcolors.WARNING}View the config stored by the script {bcolors.ENDC}\n")
    print(f"{bcolors.WARNING}##############################################{bcolors.ENDC}\n")
    print(f"{bcolors.WARNING} Examples : {bcolors.ENDC}\n")
    print(f"\t{bcolors.OKGREEN} pyeasydcer -config {bcolors.ENDC} [{bcolors.WARNING} To check existing stored configuration {bcolors.ENDC}]\n")
    print(f"\t{bcolors.OKGREEN} pyeasydcer node 1,2,3,4,5 {bcolors.ENDC} [{bcolors.WARNING} To export nodes with id 1,2,3,4,5 using the configuration user just entered or using saved config {bcolors.ENDC}]\n")
    print(f"\t{bcolors.OKGREEN} pyeasydcer node 1,2,3,4,5 -force{bcolors.ENDC} [{bcolors.WARNING} To export nodes with id 1,2,3,4,5 using the config user enters, In short -force does not use saved configuration at all {bcolors.ENDC}]\n")
    print(f"\t{bcolors.OKGREEN} pyeasydcer node 1,2,3,4,5 lando{bcolors.ENDC} [{bcolors.WARNING} For Lando Users - To export nodes with id 1,2,3,4,5 using the config user just entered or using saved config {bcolors.ENDC}]\n")
    print(f"\t{bcolors.OKGREEN} pyeasydcer node 1,2,3,4,5 -force lando{bcolors.ENDC} [{bcolors.WARNING} For Lando Users - To export nodes with id 1,2,3,4,5 using the config user enters, In short -force does not use saved configuration at all {bcolors.ENDC}]\n")   
    print(f"\t{bcolors.OKGREEN} pyeasydcer node -y {bcolors.ENDC} [{bcolors.WARNING} To export all the existing nodes using the configuration user just entered or using saved config {bcolors.ENDC}]\n")
    print(f"{bcolors.WARNING}##############################################{bcolors.ENDC}\n")


def configCheck(ask = False):
    try:
        local_config_file = os.path.join(
            os.environ["HOME"], ".pydcer_config/pydcer_settings.json"
        )
        with open(local_config_file) as file_read_object:
            pydcer_saved_config = json.load(file_read_object)
            subscription = pydcer_saved_config["subscription"]
            base_path = pydcer_saved_config["path"]
            config_saved_time = datetime.strptime(
                pydcer_saved_config["time_stamp"], "%c"
            )
            current_time = datetime.now()
            difference_in_time = (current_time - config_saved_time).seconds
            print(f"\n{bcolors.WARNING}#######################################{bcolors.ENDC}")
            if os.name == "nt":
                base_path = convertWinPath(base_path)
            if ask:
                print(f"\n{bcolors.WARNING}{bcolors.BOLD} Found a saved configuration :\n\n")
            else:
                print(f"\n{bcolors.WARNING}{bcolors.BOLD} Config being used :\n\n")
            print(f"{bcolors.WARNING}{bcolors.BOLD} Subscription: {subscription}\n Base path: {base_path}\n Config save time: {str(config_saved_time)}{bcolors.ENDC}")
            if ask:
                if difference_in_time >= 21600:
                    print(f"\n{bcolors.WARNING} Saved config is more than 6 hours old, so the script will again \n ask you to the change the config when you run the script, \n or you can use '-force' argument to change the config whenever you need{bcolors.ENDC}\n")
                else:
                    print(f"\n{bcolors.WARNING} If you want to change the config, Please use '-force' argument \n When you run the script so you can change the config when ever you want!!\n Script saves settings whenever new config is given and user will only be asked after 6 hours{bcolors.ENDC}")
            print(f"\n{bcolors.WARNING}#######################################{bcolors.ENDC}\n")
    except FileNotFoundError:
        print(f"\n{bcolors.FAIL}{bcolors.BOLD}Cannot find a saved config file, Please continue with running the script normally \nand the script will create a config file for you{bcolors.ENDC}\n")


def forceChangeConfig():
    pydcerConfig = config.checkConfig("force_change")
    pydcer_saved_config = pydcerConfig.getInfo()
    subscription = pydcer_saved_config["subscription"]
    base_path = pydcer_saved_config["path"]
    config_saved_time = datetime.strptime(pydcer_saved_config["time_stamp"], "%c")
    
    if os.name == "nt":
        base_path = convertWinPath(base_path)
    
    print(f"\n{bcolors.WARNING}#######################################{bcolors.ENDC}")
    print(f"\n{bcolors.OKGREEN} Config saved:\n\n Subscription: {subscription}\n Base Path: {base_path}\n Config save time: {str(config_saved_time)}{bcolors.ENDC}\n")
    print(f"\n{bcolors.WARNING}#######################################{bcolors.ENDC}")

def getAvailEntities():
    available_entities_config_file = os.path.join(
        os.environ["HOME"], ".pydcer_config/available_entities.txt"
    )
    with open(available_entities_config_file) as read_entity:
        avail_entities = read_entity.read().splitlines()
        print(f"\n")
        for item in avail_entities:
            print(f"{bcolors.OKGREEN}{item}{bcolors.FAIL}")
        print("\n")

def convertWinPath(path_to_be_converted):
    broken_path = path_to_be_converted.split(os.sep)
    for item in broken_path:
        if not item == "":
            if broken_path.index(item) == 0:
                base_path = "/" + item.split(":")[0]
            else:
                base_path = base_path + "/" + item
    return base_path

def main():
    global subscription, base_path, entity_type
    if len(sys.argv) == 2:
        if "-help" in sys.argv or "-h" in sys.argv:
            usage()
            sys.exit(1)
        elif "-config" in sys.argv:
            configCheck(True)
            sys.exit(1)
        elif "-force" in sys.argv:
            forceChangeConfig()
            sys.exit(1)

    if basicChecks.basicChecks() and basicChecks.checkForAvailableEntitiesText():
        if "-force" in sys.argv:
            pydcerConfig = config.checkConfig("force_change")
            sys.argv.remove("-force")
        else:
            configCheck()
            pydcerConfig = config.checkConfig()

        pydcer_saved_config = pydcerConfig.getInfo()
        subscription = pydcer_saved_config["subscription"]
        base_path = pydcer_saved_config["path"]

        if basicChecks.rootCheck(base_path, subscription):
            arguments_array = sys.argv[1:]
            entity_type = ""
            available_entities_config_file = os.path.join(
                os.environ["HOME"], ".pydcer_config/available_entities.txt"
            )
            with open(available_entities_config_file) as entity:
                available_entities = entity.read().splitlines()
                for entry in available_entities:
                    if entry in arguments_array:
                        entity_type = entry
                        arguments_array.remove(entity_type)
                        break
                if not entity_type:
                    print(f"{bcolors.FAIL}{bcolors.BOLD}\nWrong entity type detected{bcolors.ENDC}\n")
                    sys.exit(1)

            if "lando" in arguments_array:
                landoEnv = True
                arguments_array.remove("lando")
            else:
                landoEnv = False

            if len(arguments_array) == 1:
                ids_array = arguments_array[0]
            else:
                print(f"{bcolors.FAIL}{bcolors.BOLD}\nWrong input given to the script, Please use -help section{bcolors.ENDC}\n")
                sys.exit(1)

            if landoEnv:
                dcer.dcer(entity_type, ids_array.split(","), subscription, base_path, landoEnv)
            else:
                dcer.dcer(entity_type, ids_array.split(","), subscription, base_path)
        else:
            if os.name == "nt":
                base_path = convertWinPath(base_path)
            print(f"\n{bcolors.FAIL}Look's like Drupal is not properly installed, Cannot find a project with the name: {subscription} in the mentioned path: {base_path}{bcolors.ENDC}")
            sys.exit(1)
    else:
        print(f"{bcolors.FAIL}{bcolors.BOLD}\nCannot proceed further because one of the above checks failed\n{bcolors.ENDC}")
        sys.exit(1)

main()