import subprocess
import os
import glob
import shutil
from .basicChecks import bcolors
            
def exportContent(ids, entity_type, landoEnv = False):
    failedArray = []
    print(f'\n')
    for id in ids:
        if landoEnv:
            dcerCommand = 'lando drush dcer ' + entity_type + ' ' + id 
        else:
            dcerCommand = 'drush dcer ' + entity_type + ' ' + id + ' --folder=/tmp/pyeasydcer_exports/'
        exportContent = subprocess.run(dcerCommand, shell=True, capture_output=True)
        if exportContent.returncode == 0:
            if id == '-y':
                print(f'{bcolors.OKGREEN}Successfully exported default content for all existing {entity_type}{bcolors.ENDC}')
            else:
                print(f'{bcolors.OKGREEN}Successfully exported default content for a {entity_type} with id: {id}{bcolors.ENDC}')
        else:
            failedArray.append(id)
    if not len(failedArray) == 0:
        print(f'\n{bcolors.FAIL}{bcolors.BOLD}Export failed for the given id\'s: {str(failedArray)}{bcolors.ENDC}\n')
        print(f'\n{bcolors.WARNING}Rebuilding cache and trying again for the failed id\'s{bcolors.ENDC}\n')
        if landoEnv:
            cacheRebuild = subprocess.run(['lando', 'drush', 'cr'], capture_output=True)
        else:
            cacheRebuild = subprocess.run(['drush', 'cr'], shell=True, capture_output=True)
        if cacheRebuild.returncode == 0:
            for id in failedArray:
                if landoEnv:
                    dcerCommand = 'lando drush dcer ' + entity_type + ' ' + id 
                else:
                    dcerCommand = 'drush dcer ' + entity_type + ' ' + id + ' --folder=/tmp/pyeasydcer_exports/'
                exportContent = subprocess.run(dcerCommand, shell=True, capture_output=True)
                if exportContent.returncode == 0:
                    print(f'{bcolors.OKGREEN}Successfully exported default content for a {entity_type} with id: {id}{bcolors.ENDC}')
                else:
                    print(f'{bcolors.FAIL}{bcolors.BOLD}Cannot find a {entity_type} with id: {id}{bcolors.ENDC}')
            print(f'\n')
        else:
            print(f'\n{bcolors.FAIL}{bcolors.BOLD}Unable to rebuild cache, looks like there is a problem in your Drupal Installation or your lando instance is not initiated\n{bcolors.ENDC}')
    else:
        print(f'\n')
    
def appendEofAndMoveFiles(base_path, subscription, files, entity, landoEnv = False):
    for cur_file in files:
        with open(cur_file, 'a') as file_write_object:
            #check for existing EOF Pending
            file_write_object.write('\n')
        destinationPath = base_path + subscription + '/app/profiles/' + subscription + '_profile/content/' + entity + '/'
        if os.path.isdir(destinationPath):
            moveFlag = True
            shutil.copy(cur_file, destinationPath)
        else:
            moveFlag = False
    if moveFlag:
        if landoEnv:
            shutil.rmtree(base_path + subscription + '/app/' + entity)
        else:
            shutil.rmtree('/tmp/pyeasydcer_exports/' + entity)
    else:
        destinationPath = base_path + subscription + '/app/profiles/' + subscription + '_profile/content/'
        if landoEnv:
            originPath = base_path + subscription + '/app/' + entity
        else:
            originPath = '/tmp/pyeasydcer_exports/' + entity
        shutil.move(originPath, destinationPath)

def dcer(entity_type, ids, subscription, base_path, landoEnv = False):
    if landoEnv:
        available_entities_config_file = os.path.join(os.environ["HOME"], '.pydcer_config/available_entities.txt')
        with open(available_entities_config_file) as cur_entity:
            available_entities = cur_entity.read().splitlines()
        new_path = base_path + subscription + '/app/profiles/' + subscription + '_profile'
        if os.name == "nt":
            os.chdir(new_path.replace('/', os.sep))
        else:
            os.chdir(new_path)
        exportContent(ids, entity_type, landoEnv=True)
        app_path = base_path + subscription + '/app/'
        for cur_entity in available_entities:
            if os.path.isdir(app_path + cur_entity) and not os.listdir(app_path + cur_entity) == []:
                folderName = app_path + cur_entity + '/'
                filesExported = glob.glob(folderName + '*.json')
                appendEofAndMoveFiles(base_path, subscription ,filesExported, cur_entity, landoEnv = True)
            elif os.path.isdir(app_path + cur_entity) and os.listdir(app_path + cur_entity) == []:
                shutil.rmtree(app_path + cur_entity)
    else:
        new_path = base_path + subscription + '/app/profiles/' + subscription + '_profile'
        if os.name == "nt":
            os.chdir(new_path.replace('/', os.sep))
        else:
            os.chdir(new_path)
        exportContent(ids, entity_type)
        if(os.path.isdir('/tmp/pyeasydcer_exports')):
            folderToCheck = [folder for folder in os.listdir('/tmp/pyeasydcer_exports/') if os.path.isdir('/tmp/pyeasydcer_exports/' + folder) and not os.listdir('/tmp/pyeasydcer_exports/' + folder) == []]
            if folderToCheck:
                for name in folderToCheck:
                    foldername = '/tmp/pyeasydcer_exports/' + name + '/'
                    filesExported = glob.glob(foldername + '*.json')
                    appendEofAndMoveFiles(base_path, subscription ,filesExported, name)
                shutil.rmtree('/tmp/pyeasydcer_exports')
