import cv2
import time
import numpy as np
from PIL import Image, ImageGrab 
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
import glob
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
import keyboard
import requests
import json
import os
from datetime import date
from datetime import datetime
from tkinter import Tk
import win32gui, win32con

# from win32gui import GetWindowText, GetForegroundWindow



def setTemplate(path):
    template = cv2.imread(path, 0)
    return template


def waitForImage(duration , template, **options):
    if "wait" in options:
        time.sleep(options["wait"])
        
    Wait = True
    start = time.perf_counter()
    
    threshold = 0.85
    while Wait:  
        #load screenshot
        screen = np.array(ImageGrab.grab(bbox=None))
        grey_img = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]

        #Template matching
        res = cv2.matchTemplate(grey_img, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        time_elapsed =  time.perf_counter() - start

        if len(loc[0]) != 0:
            for pt in zip(*loc[::-1]):
                Wait = False
                print("point coordinate: {}".format(pt))
                cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                global poiX
                poiX = pt[0] + 236 
                global poiY 
                poiY = pt[1] + 151
            
        print(f"Time elapsed { time_elapsed }")
        
        
        if time_elapsed > duration:
            Wait = False

def leftClick(driver, **options):
    if "wait" in options:
        time.sleep(options["wait"])
        
    if("xpath" in options and options["target"]=="WebElement"):
       driver.find_element_by_xpath(options["xpath"]).click() 
       
    if ( "id" in options and options["target"]=="WebElement"):
      driver.find_element_by_css_selector(f'[id={options["id"]}]').click()    
   
    if ( "class" in options and options["target"]=="WebElement"):
      driver.find_element_by_css_selector(f'[class={options["class"]}]').click()   

        

        
def rightClick(driver, **options):
    if "wait" in options:
        time.sleep(options["wait"])
        
    if("target" not in options or options["target"] == "WebElement" ):
       action = ActionChains(driver)
       link = driver.find_element_by_xpath(options["xpath"])
       print(link)
       action.move_to_element(link)
       action.context_click(link).perform()
        
 
def waitImageRightClick(template, x , y, **options):
    
    if "wait" in options:
        time.sleep(options["wait"])
        
    Wait = True
    threshold = 0.85
    start = time.perf_counter()
    while Wait:  
        #load screenshot
        screen = np.array(ImageGrab.grab(bbox=None))
        grey_img = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]

        #Template matching
        res = cv2.matchTemplate(grey_img, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        time_elapsed =  time.perf_counter() - start

        if len(loc[0]) != 0:
            for pt in zip(*loc[::-1]):
                Wait = False
                print("point coordinate: {}".format(pt))
                cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                global poiX
                poiX = pt[0] + x 
                global poiY 
                poiY = pt[1] + y
            
        print(f"Time elapsed { time_elapsed }")
        
        
        if time_elapsed > options["duration"]:
            Wait = False
    pyautogui.moveTo(poiX, poiY, duration = 2)
    pyautogui.rightClick()
    
    
def waitImageLeftClick(template, x , y, **options):
    
    if "wait" in options:
        time.sleep(options["wait"])
        
    Wait = True
    threshold = 0.85
    start = time.perf_counter()
    while Wait:  
        #load screenshot
        screen = np.array(ImageGrab.grab(bbox=None))
        grey_img = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]

        #Template matching
        res = cv2.matchTemplate(grey_img, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        time_elapsed =  time.perf_counter() - start

        if len(loc[0]) != 0:
            for pt in zip(*loc[::-1]):
                Wait = False
                print("point coordinate: {}".format(pt))
                cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                global poiX
                poiX = pt[0] + x 
                global poiY 
                poiY = pt[1] + y
            
        print(f"Time elapsed { time_elapsed }")
        
        
        if time_elapsed > options["duration"]:
            Wait = False
    pyautogui.moveTo(poiX, poiY, duration = 2)
    pyautogui.click() 
    
          
def waitImageLeftDBClick(template, x , y, **options):
    
    if "wait" in options:
        time.sleep(options["wait"])
        
    Wait = True
    threshold = 0.85
    start = time.perf_counter()
    while Wait:  
        #load screenshot
        screen = np.array(ImageGrab.grab(bbox=None))
        grey_img = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]

        #Template matching
        res = cv2.matchTemplate(grey_img, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        time_elapsed =  time.perf_counter() - start

        if len(loc[0]) != 0:
            for pt in zip(*loc[::-1]):
                Wait = False
                print("point coordinate: {}".format(pt))
                cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                global poiX
                poiX = pt[0] + x 
                global poiY 
                poiY = pt[1] + y
            
        print(f"Time elapsed { time_elapsed }")
        
        
        if time_elapsed > options["duration"]:
            Wait = False
    pyautogui.moveTo(poiX, poiY, duration = 2)
    pyautogui.doubleClick()  
      
def enterKeystrokes(typeToSend, send, **options):
    if "wait" in options:
        time.sleep(options["wait"])
        
    if(typeToSend == "KeyComb" ):
        keyboard.press_and_release(send)
        
    if(typeToSend == "Text" ):
        keyboard.write(send)   
        
        
def get_active_window():
    _active_window_name = None
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        _active_window_name = win32gui.GetWindowText(window)
    else:
        print("sys.platform={platform} is not supported."
              .format(platform=sys.platform))
        print(sys.version)
    return _active_window_name


def repeat(times, action, **options):
    interval = 0.1
    if "wait" in options:
        time.sleep(options["wait"])
    if "interval" in options:
        interval = options["interval"]
        
               
    for x in range(times):
        action()
        time.sleep(interval)


def pasteToVariable(**options): 
    if "wait" in options:
        time.sleep(options["wait"])  
          
    root = Tk()
    # keep the window from showing
    root.withdraw()
    # read the clipboard
    variable = root.clipboard_get()     
    return variable


def sendMsg(**options):
    data = {
        "recipient":options["mailList"] ,
        "recipientName":"GoDigi Staff",
        "subject":options["subject"],
        "message": options["message"] 
    } 
    # sending post request and saving response as response object 
    r = requests.post(url = "http://ghprddigintfsrv.gh.sbicdirectory.com/emailer/rpa/sendmail.php", data = json.dumps(data))
    print(r.text)
    


def queryToCSV(path_name, query, **options):
    #create file
    f = open(f"{path_name}.csv", "w")
    f.close()
    #add Columns
    if "headers" in options:
        name = ''
        for columnName in options["headers"]:
            name += f"{columnName},"
        f = open(f"{path_name}.csv", "a")
        f.write(f"{name}\n") 
        f.close()
    #add Lines
    for index,  row in enumerate(query):
        line = ""
        for entry in row:

            line += f"{entry},"    
        f = open(f"{path_name}.csv", "a")
        f.write(f"{line}\n")    
        f.close()
    #filter no of Lines    
        if("rows" in options):
            if(index == (1 + options["rows"])):
                break
            
def getPathToDir():
    return os.path.dirname(os.path.abspath(__file__))

def getDatestr(Format):
    today = date.today()
    todays_date = today.strftime(Format)
    return todays_date


def getTimestr(Format):
    now = datetime.now()
    current_time = now.strftime(Format)
    return current_time

def getDateTimestr(*arg):
    if len(arg) != 0:
       Format =  arg[0]  
    else:
       Format = "%d/%m/%Y %H:%M:%S"  
          
    now = datetime.now()
    dt_string = now.strftime(Format)
    return dt_string


def fileUpload(fileName, docType, sourceCode):
    headers = {
           "sourceCode": f"{sourceCode}"
           }
    url = f"https://ghuatgodigisrv1.gh.sbicdirectory.com:9982/FileServices/File/upload?documenttype={docType}"
    files = { 'file': open(fileName, 'rb')} 
    r = requests.post(url,  headers = headers, verify = False, files = files )
    print(r.text)
    return json.loads(r.text)['filePath']


def postMonitorUpdates(name, code):
    data = {
        "botCode": code,
        "botName":name,
        "lastRun": f"{getDateTimestr()}"
    } 
    print(data)
    r = requests.post(url = "http://ghprddigintfsrv.gh.sbicdirectory.com:8019/updateBotStatus", data = data)
    print(r.text)    
    
def createDirectory(dirName, **options):
        cwd = os.getcwd()
        if "target" in options:
            os.chdir(options["target"]) 
        try:
            # Create target Directory
            os.mkdir(dirName)
            print("Directory " , dirName ,  "created ")  if "target" in options else print("Directory " , dirName ,  " created in ", options["target"])
        except FileExistsError:
            print("Directory " , dirName ,  " already exists")   
        
        if "target" in options:
            os.chdir(cwd) 
            
def rename(oldName, newName, **options):  
    if "target" in options:
        cwd = options["target"] 
        
    else:
        cwd = os.getcwd()    
    try:
            # Create target Directory
        if os.path.exists(cwd):
            os.rename(f"{cwd}\\{oldName}", f"{cwd}\\{newName}")
            if "target" in options:
                print(f"'{oldName}' is renamed to '{newName}' in path {options['target']}")
            else :
                print("'{0}' is renamed to '{1}'".format(oldName, newName)) 
    except FileNotFoundError:
            print("Directory does not exist") 
 
 
def getLatestFile(**options):
    if "path" in options:
        cwd = options["path"]      
    else:
        cwd = os.getcwd()  
    if "ext" in options:    
        list_of_files = glob.glob(f'{cwd}\\*.{options["ext"]}')
    else:
       list_of_files = glob.glob(f'{cwd}\\*')  
    try:      
        latest_file = max(list_of_files, key = os.path.getctime).replace(f'{cwd}\\','')
        return latest_file
    except  ValueError:
       return "Directory is empty"
    
 
def getListofFiles(**options):
    list_of_files = []
    if "path" in options:
        cwd = options["path"]      
    else:
        cwd = os.getcwd()  
    if "ext" in options:    
        list_of_files = glob.glob(f'{cwd}\\*.{options["ext"]}')
    else:
       list_of_files = glob.glob(f'{cwd}\\*') 
    return list_of_files    
       
def writeToSplunk(start, process_name, success):
    splunkObject ={ 
    "host":"ghagodigibkgsrv.gh.sbicdirectory.com",
    "event":{
        "attended":"No",
        "bot_type":"Python",
        "solution_type":"RPA",
        "process_name":process_name,
        "bot_machine":"ghagodigibkgsrv.gh.sbicdirectory.com",
        "bot_user":"GoDigiAdmin",
        "country":"Ghana",
        "passed":success,
        "start":start,
        "end": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "heartbeat":"1"
      },
    "source":"http:rpa_aria",
    "sourcetype":"_json",
    "index":"rpa_aria"
   }
    
    
    f = open(r"C://java//log.txt", "w")
    f.write(json.dumps(splunkObject))
    f.close()
    os.system(r"C://java//write_event_to_splunk.exe") 


# Test getLastestFile()   
# latest_file = getLatestFile()
# print(latest_file)  


        
# Test waitforImage()
template = setTemplate("image.jpg")
waitImageLeftDBClick(template, 36 ,  55, duration = 10)
# waitForImage(10,template, wait =2) 

#Test maximize
# win32gui.GetWindowText (win32gui.GetForegroundWindow())
# hwnd = win32gui.GetForegroundWindow()
# win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
# print (str(win32gui.GetWindowText (win32gui.GetForegroundWindow())))   
# window = win32gui.GetForegroundWindow()
# win32gui.ShowWindow(window, win32con.SW_MAXIMIZE)
