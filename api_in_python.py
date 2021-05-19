'''
#WORKING WITH APIS
import json
def con(s):
    s=json.dumps(s,indent=2)
    print(s)
import requests
#params={"district_id":"265","date":"10-05-2021"}
#params={"state_id":"16"}
#passing a x-api-key. No need to pass value 2 methods
headers={"Authorization":"3sjOr2rmM52GzhpMHjDEE1kpQeRxwFDr4YcBEimi sreyans","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51"}
headers={"pragma":"no-cache","Authorization":"x-api-key sreyans","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51"}
#response=requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict",params=params,headers=headers)
response=requests.get("https://api.demo.co-vin.in/api/v2/admin/location/districts/16",headers=headers)
print(response)
con(response.json())
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import requests
from datetime import datetime,date,timedelta
import time
from time import sleep

def send_whatsapp_message(event):
    #x=["Darsh Bakul Mehta Christ University, CMA"]
    x=["me"]
    PATH="C:\Program Files (x86)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=C:/Users/sreya/yo/User_Data')

    driver = webdriver.Chrome(executable_path=PATH,options=options)
    driver.get('https://web.whatsapp.com/')
    try:
        #wait for max 200s
        #whatsapp loads but the search button does not appear and hence WebDriverWait to wait until search loads
        initi = WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]")))
        #initi = WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.CLASS_NAME, "C28xL")))
        for target in x:
            print("Wishing",target,"on their",event)
            input_box_search=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]')
            input_box_search.click()
            input_box_search.send_keys(target,Keys.ENTER)
            print("Target Successfully Selected")
            sleep(1)

            inp_xpath = "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]"
            input_box = WebDriverWait(driver,20).until(EC.presence_of_element_located((
                By.XPATH, inp_xpath)))
            sleep(0.5)
            for string in event:
                input_box.send_keys(string)
                sleep(0.5)
                input_box.send_keys(Keys.SHIFT+Keys.ENTER)
            time.sleep(0.5)
            input_box.send_keys(Keys.ENTER)
            time.sleep(2)
            print("Successfully Send Message to : "+ target + '\n')
            print("DONE")
    except Exception as E:
        print(E)
    finally:
        print("DONE all")
        #whenever qr code dena padega, usko driver.quit() nahi karke
        #khud hi quit karna hoga->manually
        driver.quit()

t=date.today()+timedelta(days=1)
t=t.strftime("%d-%m-%Y")
#print(t)

params1={"district_id":294,"date":t}
params2={"district_id":265,"date":t}
keyval=0
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51"}
flag=2
while(flag):
    if keyval:
        response=requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict",headers=headers,params=params2)
    else:
        response=requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict",headers=headers,params=params1)
    print(response)
    final=response.json()
    #print(*final)
    
    if final["sessions"]:
        di=[]
        vals=0
        for i in final["sessions"]:
            if i['available_capacity'] and i['min_age_limit']==18:
                if vals:
                    di.append(str({"date":t,"Name":i['name'],"1st dose capacity":i['available_capacity_dose1'],"2nd dose capacity":i['available_capacity_dose2'],"Address":i['address'],"Fees":i['fee'],"Vaccine":i["vaccine"]}))
                else:
                    di.append(str({"date":t,"Name":i['name'],"1st dose capacity":i['available_capacity_dose1'],"2nd dose capacity":i['available_capacity_dose2'],"Address":i['address'],"Fees":i['fee'],"Vaccine":i["vaccine"]}))
                vals^=1
        #print(*di)
        if di:
            send_whatsapp_message(di)
    flag-=1
    sleep(1)
    keyval^=1

'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import requests
from datetime import datetime,date,timedelta
import time
from time import sleep
from tabulate import tabulate

def send_whatsapp_message(event):
    #x=["Darsh Bakul Mehta Christ University, CMA"]
    x=["me"]
    PATH="C:\Program Files (x86)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=C:/Users/sreya/yo/User_Data')
    event=tabulate(event,headers=["date","name","DOSE1 cap","DOSE2 cap","address","fee","vaccine"])
    driver = webdriver.Chrome(executable_path=PATH,options=options)
    driver.get('https://web.whatsapp.com/')
    try:
        #wait for max 200s
        #whatsapp loads but the search button does not appear and hence WebDriverWait to wait until search loads
        initi = WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]")))
        #initi = WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.CLASS_NAME, "C28xL")))
        for target in x:
            #print("Wishing",target,"on their",event)
            print(event)
            input_box_search=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]')
            input_box_search.click()
            input_box_search.send_keys(target,Keys.ENTER)
            print("Target Successfully Selected")
            sleep(1)

            inp_xpath = "/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]"
            input_box = WebDriverWait(driver,20).until(EC.presence_of_element_located((
                By.XPATH, inp_xpath)))
            sleep(0.5)
            input_box.send_keys(event)
            sleep(0.5)
            input_box.send_keys(Keys.SHIFT+Keys.ENTER)
            time.sleep(0.5)
            input_box.send_keys(Keys.ENTER)
            time.sleep(2)
            print("Successfully Send Message to : "+ target + '\n')
            print("DONE")
    except Exception as E:
        print(E)
    finally:
        print("DONE all")
        #whenever qr code dena padega, usko driver.quit() nahi karke
        #khud hi quit karna hoga->manually
        driver.quit()

t=date.today()#+timedelta(days=1)
t=t.strftime("%d-%m-%Y")
#print(t)

params1={"district_id":294,"date":t}
params2={"district_id":265,"date":t}
keyval=0
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51"}
flag=2
while(flag):
    if keyval:
        response=requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict",headers=headers,params=params2)
    else:
        response=requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict",headers=headers,params=params1)
    print(response)
    final=response.json()
    #print(*final)
    
    if final["sessions"]:
        di=[]
        for i in final["sessions"]:
            if i['available_capacity'] and i['min_age_limit']==18:
                di.append([str(t),i['name'],i['available_capacity_dose1'],i['available_capacity_dose2'],i['address'],i['fee'],i["vaccine"]])
        #print(*di)
        if di:
            send_whatsapp_message(di)
    flag-=1
    #sleep(5)
    keyval^=1
'''
