# DEPENDENCIES
from AppKit import NSWorkspace
from subprocess import Popen, PIPE
import time
from activity import *
from Foundation import *
import json
from datetime import date,datetime 
import os
#https://www.haskell.org/arrows/syntax.html

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
def cd_to_script_dir():
    """Change to directory the script is running from

    Returns:
        [str] -- [path to script directory]
    """
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    return dname

def handle_data_file(today):
    """
    str --> Creates or reads file --> dictionary \n
    This function returns the data of the file given into it. \n
    If the file does not exit it is created. \n
    today is in the format 2020-05-14
    """
   
    cd_to_script_dir()
    files_in_data = os.listdir()
    filenames = str(today) + ".json"
    if filenames in files_in_data:
        if os.stat(filenames).st_size == 0:
            return {}
        else:
            with open(filenames,"r") as f:
                return json.load(f)
    else:
        with open(filenames, 'w+') as f:
            return {}


def dump_into_file(today,datas):
    """
    str --> Dumps into file --> dictionary \n
    This function writes to a file \n
    today is in the format 2020-05-14
    """
    filenames = str(today) + ".json"
    with open(filenames, 'w') as f:
        json.dump(datas, f, indent=4)
    time.sleep(10)
    main()
def throw_in_json(app, link, time_stamps, productive):
    now = datetime.now()
    today = now.strftime("%H:%M")
    todays = date.today()
    data = handle_data_file(todays)
    if app != "Google Chrome":
        data[str(today)] = {
            "Appilication":app,
            "Productive":productive
        }
    

    else:
        data[str(today)] = {
            "Appilication":link,
            "Productive":productive
        }


    dump_into_file(todays, data)

#testing testing testing     
def find_application_name():
    """
    Returns active app_name
    """
    return NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
def main():
    activeAppName = find_application_name()
    time_stamp = datetime.now()
    print(activeAppName)
    browsers = ["Google Chrome","Safari","Firefox","Edge"]
    productive = ["Code", "Google Chrome", "henrico.schoology.com"]
    not_productive = ["youtube.com"]
    new_url = ""
    if activeAppName in browsers:
        
        unnew_url = google_url(activeAppName)
        new_url = str(unnew_url).split("/")[2]
        print(new_url)
    is_productive = ""
    if activeAppName in productive:
        is_productive = "Yes"
    elif activeAppName in not_productive:
        is_productive = "No"
    else:
        is_productive = "No"
    throw_in_json(activeAppName, new_url, time_stamp, is_productive)

#RUNNER
if __name__ == "__main__":
    main()
 