# DEPENDENCIES
from AppKit import NSWorkspace
from subprocess import Popen, PIPE
import time
from activity import *
from Foundation import *
import json
from datetime import date,datetime 
import os
#FUNCTIONS
def run_this_scpt(scpt, args=[]):
    p = Popen(['osascript', '-'] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(scpt)
    return stdout

def google_url(activeAppName): #https://stackoverflow.com/questions/2940916/how-do-i-embed-an-applescript-in-a-python-script
    #tell application "Google Chrome" to return URL of active tab of front window
    textOfMyScript = "tell application \"".encode()+activeAppName.encode()+"\" to get the url of the active tab of window 1".encode()
    result = run_this_scpt(textOfMyScript)
    # res = ''.join(format(ord(i), 'b') for i in textOfMyScript) 
    # p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    # s = NSAppleScript.initWithSource_(
    #     NSAppleScript.alloc(), textOfMyScript)
    # results, err = s.executeAndReturnError_(None)
    return result


def handle_data_file(today):
    """
    str --> Creates or reads file --> dictionary \n
    This function returns the data of the file given into it. \n
    If the file does not exit it is created. \n
    today is in the format 2020-05-14
    """
    os.chdir("/Users/srikarkarra/Downloads/Important Stuff/Coding/timetracking/data_for_tracking_time")
    files_in_data = os.listdir()
    filenames = str(today) + ".json"
    if filenames in files_in_data:
        pass 
        # if os.stat(filenames).st_size == 0:
        #     return {}
        # else:
        #     with open(filenames,"r") as f:
        #         return json.load(f)
    else:
        with open(filenames, 'w+') as f:
            return {}


def dump_into_file(today,datas, appz, linkzs):
    """
    str --> Dumps into file --> dictionary \n
    This function writes to a file \n
    today is in the format 2020-05-14
    """
    filenames = str(today) + ".json"
    with open(filenames, 'a') as f:
        json.dump(datas, f, indent=4)
    time.sleep(5)
    main(appz, linkzs)
def throw_in_json(app, link, productive):
    now = datetime.now()
    today = now.strftime("%H:%M")
    todays = date.today()
    data = handle_data_file(todays)
    datas = {}
    if app != "Google Chrome":
        datas[str(today)] = {
            "Appilication":app,
            "Productive":productive
        }
    

    else:
        datas[str(today)] = {
            "Appilication":link,
            "Productive":productive
        }


    dump_into_file(todays, datas, app, link)

#testing testing testing     
def find_application_name():
    """
    Returns active app_name
    """
    return NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']

def productive(activeAppNames, linkz):
    productive = ["Code", "henrico.schoology.com", "stackoverflow.com", "mail.google.com"]
    not_productive = ["youtube.com", "reddit.com", "netflix.com"]
    is_productive = False
    if activeAppNames != "Google Chrome":
        if activeAppNames in productive:
            is_productive = True 
        elif activeAppNames in not_productive:
            is_productive = False
        else:
            is_productive = False
    else:
        if linkz in productive:
            is_productive = True 
        elif linkz in not_productive:
            is_productive = False
        else:
            is_productive = False
    return is_productive
        


def main(currentAppName, currentURL):
    browsers = ["Google Chrome","Safari","Firefox","Edge"]

    activeAppName = find_application_name()
    if activeAppName != currentAppName or activeAppName == "Google Chrome": 
        if activeAppName in browsers:
            unnew_url = google_url(activeAppName)
            new_url = str(unnew_url).split("/")[2]
            if new_url != currentURL:
                currentURL = new_url
                print(new_url)
                is_productives = productive(currentAppName, currentURL)
                throw_in_json(currentAppName, currentURL, is_productives)
        else:
            currentAppName = activeAppName
            print(activeAppName)
            is_productives = productive(currentAppName, "")
            throw_in_json(currentAppName, "", is_productives)
    


#RUNNER
if __name__ == "__main__":
    main("", "")
 